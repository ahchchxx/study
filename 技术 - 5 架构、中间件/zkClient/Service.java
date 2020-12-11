package com.example.demo.zkClient;

import java.io.IOException;

import org.I0Itec.zkclient.ZkClient;

public class Service {

	public static void main(String[] args) throws IOException {
		Service service = new Service();
		service.init();
		
		System.in.read();
	}

	private String serviceName = "order-service";
	public void init() {
		String serverList = "172.21.140.18:2181";// localhost:2180
		String path = "/config";
		
		ZkClient zkClient = new ZkClient(serverList);
		if (!zkClient.exists(path)) {
			zkClient.createPersistent(path);
		}
		
		if (!zkClient.exists(path + "/" + serviceName)) {
			zkClient.createPersistent(path + "/" + serviceName);
		}
		
		String ip = "127.0.0.11:8080";
		zkClient.createEphemeral(path + "/" + serviceName + "/" + ip);
		
		System.out.println("订单服务发布成功：" + path + "/" + serviceName + "/" + ip);
	}
}
