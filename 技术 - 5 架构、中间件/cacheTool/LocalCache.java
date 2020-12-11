package com.example.demo.test1;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Map.Entry;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
 
/**
 * 简易本地缓存的实现类
 * 
 * @author zhangwei_david
 * @version $Id: LocalCache.java, v 0.1 2014年9月6日 下午1:04:53 zhangwei_david Exp $
 */
public class LocalCache {
	// 默认的缓存容量
	private static int DEFAULT_CAPACITY = 512;
	// 最大容量
	private static int MAX_CAPACITY = 100000;
	// 刷新缓存的频率
	private static int MONITOR_DURATION = 10;// 10 S，TimeUnit.SECONDS.sleep
	// 启动监控线程
	static {
		new Thread(new TimeoutTimerThread()).start();
	}
	// 使用默认容量创建一个 Map
	private static ConcurrentHashMap<String, CacheEntity> cache = 
			new ConcurrentHashMap<String, CacheEntity>(DEFAULT_CAPACITY);

	// example
	public static void main(String[] args) {
		LocalCache.setValue("a", 1);
		System.out.println(LocalCache.getValue("a"));
		LocalCache.setValue("a", 2);
		System.out.println(LocalCache.getValue("a"));
		LocalCache.setValue("a1", "asdf", 10);
		System.out.println(LocalCache.getValue("a1"));
	}

	/**
	 * 从本地缓存中获取key对应的值，如果该值不存则则返回null
	 * @param key
	 * @return
	 */
	public static Object getValue(String key) {
		return cache.get(key).getValue();
	}
	public static boolean isExsitValue(String key) {
		return (cache.get(key) == null) ? false : true;
	}
	/**
	 * 将key-value 保存到本地缓存并制定该缓存的过期时间
	 * @param key
	 * @param value
	 * @param expireTime 过期时间，单位:秒，如果是-1 则表示永不过期
	 * @return
	 */
	public static boolean setValue(String key, Object value, int expireTime) {
		return putCloneValue(key, value, expireTime);
	}
	public static boolean setValue(String key, Object value) {
		return setValue(key, value, -1);
	}
 
	/**
	 * 清空所有
	 */
	public void clear() {
		cache.clear();
	}
 
	/**
	 * 将值通过序列化clone 处理后保存到缓存中，可以解决值引用的问题
	 * @param key
	 * @param value
	 * @param expireTime
	 * @return
	 */
	private static boolean putCloneValue(String key, Object value, int expireTime) {
		try {
			if (cache.size() >= MAX_CAPACITY) {
				return false;
			}
			// 序列化赋值
			CacheEntity entityClone = clone(new CacheEntity(value, System.nanoTime(), expireTime));
			cache.put(key, entityClone);
			System.out.println("新增缓存 " + key + " ： " + value.toString());
			return true;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return false;
	}
	/**
	 * 序列化 克隆处理
	 * @param object
	 * @return
	 */
	@SuppressWarnings("unchecked")
	private static <T extends Serializable> T clone(T object) {
		T cloneObject = null;
		try {
			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			ObjectOutputStream oos = new ObjectOutputStream(baos);
			oos.writeObject(object);
			oos.close();
			ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
			ObjectInputStream ois = new ObjectInputStream(bais);
			cloneObject = (T) ois.readObject();
			ois.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return cloneObject;
	}
	
 
	/**
	 * 过期处理线程
	 * 
	 * @author Lenovo
	 * @version $Id: LocalCache.java, v 0.1 2014年9月6日 下午1:34:23 Lenovo Exp $
	 */
	static class TimeoutTimerThread implements Runnable {
		public void run() {
			while (true) {
				try {
//					System.out.println("Cache monitor");
					TimeUnit.SECONDS.sleep(MONITOR_DURATION);
					checkTime();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
 
		/**
		 * 过期缓存的具体处理方法
		 * @throws Exception
		 */
		private void checkTime() throws Exception {
			// 开始处理过期
			// for (String key : cache.keySet()) {
			for(Entry<String, CacheEntity> entry : cache.entrySet()) {
				CacheEntity tce = entry.getValue();// cache.get(key);
				System.out.println("check cache: " + entry.getKey() + "-" + tce.getValue() + "-" + tce.getGmtModify() + "-" + tce.getExpire());
				if (tce.getExpire() == -1) {
					continue;
				}
				long timoutTime = TimeUnit.NANOSECONDS.toSeconds(System.nanoTime() - tce.getGmtModify());
				// "过期时间 : " + timoutTime;
				if (tce.getExpire() > timoutTime) {
					continue;
				}
				System.out.println("清除过期缓存 ： " + entry.getKey());
				// 清除过期缓存和删除对应的缓存队列
				cache.remove(entry.getKey());// key
			}
		}
	}
}