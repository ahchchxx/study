package com.example.demo.zkClient;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.I0Itec.zkclient.IZkChildListener;
import org.I0Itec.zkclient.ZkClient;

public class Consumer {
	private String serviceName = "order-service";
	private List<String> serviceList = new ArrayList<String>();

	public static void main(String[] args) throws InterruptedException {
		Consumer consumer = new Consumer();
		consumer.init();
		while(true) {
			consumer.consume();
			Thread.sleep(1000);
		}
	}

	public void init() {
		String serverList = "172.21.140.18:2181";// localhost:2180
		String path = "/config/" + serviceName;// zNode
		
		ZkClient zkClient = new ZkClient(serverList);
		if (zkClient.exists(path)) {
			serviceList = zkClient.getChildren(path);
		} else {
			throw new RuntimeException("service not found");
		}
		
		zkClient.subscribeChildChanges(path, new IZkChildListener() {
			@Override
			public void handleChildChange(String parentPath, List<String> list) throws Exception {
				System.out.println("service change");
				serviceList = list;
				System.out.println(list.toString());
			}
		});
	}
	public void consume() {
		if (serviceList.size() < 1) {
			return;
		}
		Random random = new Random();
		int index = random.nextInt(serviceList.size());
		System.out.println("调用指定服务：" + serviceList.get(index));
	}
}
