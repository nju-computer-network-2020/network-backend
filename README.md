# network-backend

## 接口说明

- 连接 telnet

  ```json
  url: "/connect",
  params: {
      "hostname": "RTA|RTB|RTC",
      "ipAdd": "172.16.0.1",
      "password": "123456"
  },
  result: {
      "success": true,
      "errMessage": "ipErr|invalidPasswd"
  }
  ```

  - 前端请求一定要和 "RTA|RTB|RTC" 中的一个匹配。
  - `ipErr` 表示地址有问题， `invalidPasswd` 表示密码有问题。

- 一键执行配置

  ```json
  url: "/autoConfig",
  result: {
      "success": true,
      "errMessage": "hostIncomplete|ipErr|invalidPasswd|" 
  }
  ```

  - `hostIncomplete` 表示没有给所有的路由器都输入相应的 telnet 地址和密码。

- 获取测试结果（待定）

  ```json
  url: "/testResult",
  result: {
      "message": ""
  }
  ```

  

