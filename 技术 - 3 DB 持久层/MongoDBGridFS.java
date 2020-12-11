package com.example.demo.mongoDB;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.gridfs.GridFS;
import com.mongodb.gridfs.GridFSInputFile;
import org.bson.Document;

import java.io.*;

public class MongoDBGridFS {// ClientGridFS

    GridFS fs;
    MongoCollection<Document> collection;

    public void setUp() {
        MongoClient mongoClient = new MongoClient("192.168.0.189", 27017);
        //连接到数据库
        DB db = mongoClient.getDB("leo");
        fs = new GridFS(db);

        collection = MongoDBUtil.getConnect().getCollection("fs.files");
    }

    /**
     * mongofiles put xxx.txt
     * 上传文件
     *
     * @throws IOException
     */
    public void put() throws IOException {
        File file = new File("d:\\zookeeper-3.4.10.tar.gz");
        GridFSInputFile gfFile = fs.createFile(file);
        gfFile.save();
    }

    /**
     * mongofiles get xxx.txt
     * 下载文件
     * 也可以拆成 2个表，一个记录文件基本信息，一个存储文件内容
     * 
     *
     * @throws IOException
     */
    public void get() throws IOException {
        File file = new File("d:\\zookeeper-3.4.10_down.tar.gz");
        FileOutputStream os = new FileOutputStream(file);
        //获得文件流
        InputStream is = fs.findOne(new BasicDBObject("filename", "zookeeper-3.4.10.tar.gz")).getInputStream();
        //下载
        byte[] bytes = new byte[1024];
        while (is.read(bytes) > 0) {
            os.write(bytes);
        }
        os.flush();
        os.close();
    }

    /**
     *  mongofiles list xx.txt
     * 查看文件
     */
    public  void list(){
        FindIterable findIterable = collection.find();
        MongoCursor cursor = findIterable.iterator();
        while (cursor.hasNext()) {
            Document document = (Document) cursor.next();
            System.out.println(document.get("filename"));
        }
    }

    /**
     * mongofiles delete xxx.txt
     * 删除文件
     */
    public void delete(){
        fs.remove("zookeeper-3.4.10.tar.gz");
    }

}

