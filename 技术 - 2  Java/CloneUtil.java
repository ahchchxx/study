// 对象克隆，
// 1）重写 clone() 方法
// 2）实现 serializable 接口


import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

public class CloneUtil {

  @SuppressWarnings("unchecked")
  public static <T extends Serializable> T clone(T obj) throws Exception {
    ByteArrayOutputStream bout = new ByteArrayOutputStream();
    ObjectOutputStream oos = new ObjectOutputStream(bout);
    oos.writeObject(obj);
    ByteArrayInputStream bin = new ByteArrayInputStream(bout.toByteArray());
    ObjectInputStream ois = new ObjectInputStream(bin);
    return (T)ois.readObject();
  }
  
}
