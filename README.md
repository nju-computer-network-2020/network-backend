# network-backend

## 接口说明

- 连接 telnet

  ```json
  url: "/connect",
  params: {
      hostname: "RTA|RTB|RTC", // 注意区分大小写，且只能从列出的值中选择
      ipAdd: "172.16.0.1",
      password: "123456"
  },
  result: {
      success: true,
      errMessage: "ipErr|invalidPasswd" // ipErr 表示地址有问题， invalidPasswd 表示密码有问题
  }
  ```

- 一键执行配置

  ```json
  url: "/autoConfig",
  result: {
      success: true,
      errMessage: "hostIncomplete|ipErr|invalidPasswd|" 
      // hostIncomplete 表示没有给所有的路由器都输入相应的 telnet 地址和密码
  }
  ```

- 获取测试结果（待定）

  ```json
  url: "/testResult",
  result: {
      message: "",
      // 其他待定
  }
  ```

  

