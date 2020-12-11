package com.cares.intelligentairport.tools.json.comm;

import com.cares.intelligentairport.tools.json.param.CommandData;
import com.cares.intelligentairport.tools.json.param.Item;
import com.cares.intelligentairport.tools.json.param.Row;

import java.lang.reflect.Field;
import java.util.Date;

// javabean 和 其它类型的互转
// 主要用到反射的知识，读写值
// 		类：Class
// 		子类与父类：Class
// 		实现的接口：Interface
//		构造函数：Constructor
//		变量：Field
//		方法：Method
//			方法的形参：method.getTypeParameters() 
//		注解：Annotation，@interface 里面定义的未实现的方法，可以设置这个方法值，像变量一样用
//			注解可以加在类、变量、方法、参数等上面
public class BeanUtil {
    /**
     * 从 Row 读信息到 obj 中
     * @param row
     * @param obj
     */
    public boolean rowToBean(Row row, Object obj) {
        if (obj == null || row == null) {
            return false;
        }
        for (Field f : obj.getClass().getDeclaredFields()) {
            String name = f.getName();
            System.out.println(f.getName());
            try {
                Item item = new Item("");
                boolean exit = false;
                if (row.existColumn(name)) {
                    item = row.getColumn(name);
                    exit = true;
                }
                if(exit){
                    f.setAccessible(true);
                    Object value = this.getObject(f.getType(), item.getStringColumn().trim());
                    f.set(obj, value);
                }
            } catch(Exception ex) {
                return false;
            }
        }
        return true;
    }
    /**
     * 从 CommandData 读信息到 obj 中
     * @param data
     * @param obj
     */
    public boolean dataToBean(CommandData data, Object obj) {
        if (obj == null || data == null) {
            return false;
        }
        for (Field f : obj.getClass().getDeclaredFields()) {
            String name = f.getName();
            System.out.println(f.getName());
            try {
                Item item = new Item("");
                boolean exit = false;
                if (data.existItem(name)) {
                    item = data.getParm(name);
                    exit = true;
                }
                if(exit){
                    f.setAccessible(true);
                    Object value = this.getObject(f.getType(), item.getStringColumn().trim());
                    f.set(obj, value);
                }
            } catch(Exception ex) {
                return false;
            }
        }
        return true;
    }

    /**
     * @Title: beatToData
     * @Description: 将当前类中所有字段数据写入输出参数中
     * @param data 输出参数
     */
    public void beanToData(CommandData data, Object obj) {
        for(Field f : obj.getClass().getDeclaredFields()) {
            String name = f.getName();
            try {
                f.setAccessible(true);
                Object value = f.get(obj);
                data.addParm(name, value.toString());
            } catch(Exception ex) {
            }
        }
    }

    /**
     * @Title: getObject
     * @Description: 将字符串转化成指定字段的类型
     * @param type 字段类型
     * @param value 字符串
     * @return 转化后对象
     */
    public Object getObject(Class<?>type,String value){
        if (type.equals(int.class) || type.equals(Integer.class)) {
            return Unit.getInteger(value);
        } else if(type.equals(float.class) || type.equals(Float.class)) {
            return Unit.getFloat(value);
        } else if(type.equals(long.class) || type.equals(Long.class)) {
            return Unit.getLong(value);
        } else if(type.equals(double.class) || type.equals(Double.class)) {
            return Unit.getDouble(value);
        } else if(type.equals(String.class)) {
            return value;
        } else if(type.equals(Date.class)) {
            return Unit.getDate(value);
        }
        return value;
    }
	
	
	
	
	/**
	 * 从 CommandData 读信息到 obj 中
	 * @param data
	 * @param obj
	 */
	public static void readData(CommandData data, Object obj) {
		if(obj == null || data == null) {
			return;
		}
		for(Field f :obj.getClass().getDeclaredFields()) {
			try
			{
				PropertyDescriptor pd = new PropertyDescriptor(f.getName(), obj.getClass());
				String name = pd.getName();
				Method write = pd.getWriteMethod();
				if(write != null && data.existItem(name)) {
					if(pd.getPropertyType() == String.class) {
						write.invoke(obj, data.getParm(name).getStringColumn());
					}
					else if(pd.getPropertyType() == int.class || pd.getPropertyType() == Integer.class) {
						write.invoke(obj, data.getParm(name).getIntegerColumn());
					}
					else if(pd.getPropertyType() == long.class) {
						write.invoke(obj, data.getParm(name).getLongColumn());
					}
					else if(pd.getPropertyType() == float.class) {
						write.invoke(obj, data.getParm(name).getDoubleColumn());
					}
					else if(pd.getPropertyType() == double.class) {
						write.invoke(obj, data.getParm(name).getDoubleColumn());
					}
					else if(pd.getPropertyType() == Date.class) {
						write.invoke(obj, data.getParm(name).getDateColumn());
					}
				}
			}
			catch(Exception ex) {
			}
		}
	}
	/**
	 * 读取 obj，向 data 写入信息
	 * @param obj
	 * @param data
	 */
	public static void writeData(Object obj, CommandData data) {
		if(obj == null || data == null) {
			return;
		}
		for(Field f : obj.getClass().getDeclaredFields()) {
			try
			{
				PropertyDescriptor pd = new PropertyDescriptor(f.getName(),obj.getClass());
				String name = pd.getName();
				Method read = pd.getReadMethod();
				if(read != null) {
					if(pd.getPropertyType() == String.class) {
						data.addParm(name,(String)read.invoke(obj));
					}
					else if(pd.getPropertyType() == int.class) {
						data.addParm(name,(int)read.invoke(obj));
					}
					else if(pd.getPropertyType() == long.class) {
						data.addParm(name,(long)read.invoke(obj));
					}
					else if(pd.getPropertyType() == float.class) {
						data.addParm(name,(double)read.invoke(obj));
					}
					else if(pd.getPropertyType() == double.class) {
						data.addParm(name,(double)read.invoke(obj));
					}
					else if(pd.getPropertyType() == Date.class) {
						data.addParm(name,(Date)read.invoke(obj));
					}
				}
			}
			catch(Exception ex) {
				
			}
		}
	}
	
	
	
}

