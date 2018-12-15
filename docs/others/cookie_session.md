# cookie 和 session 的自动登录机制

> cookie 是浏览器本地存储机制，存在域名之下，存储不安全（明文）。
  服务器在返回id时通过规则生成一串字符（密文），并设置了过期时间。存储在服务器端(数据库)

## HTTP

### http 请求是一种无状态的请求

用户向服务器发起的请求之间是没有状态的。也就是服务器并不知道这是同一个用户发的。

为了分辨链接是谁发起的，需自己去解决这个问题。不然有些情况下即使是同一个网站每
打开一个页面也都要登录一下。而Session和Cookie就是为解决这个问题而提出来的两个机制。

## cookie

大多数浏览器，每个域不要超过50个cookie，每个域不要超过4093个字节 。 也就是说，所有cookie的大小不应该超过4093字节。

### cookie 是浏览器支持的一种本地存储方式

##  cookie 机制

cookie 机制采用的是在客户端保持状态的方案

正统的cookie分发是通过扩展HTTP协议来实现的，服务器通过在HTTP的响应头中加上一行特殊的指示以提示

浏览器按照指示生成相应的cookie。然而纯粹的客户端脚本如JavaScript或者VBScript也可以生成cookie。而cookie的使用

是由浏览器按照一定的原则在后台自动发送给服务器的。浏览器检查所有存储的cookie，如果某个cookie所声明的作用范围

大于等于将要请求的资源所在的位置，则把该cookie附在请求资源的HTTP请求头上发送给服务器。
 
cookie的内容主要包括：名字，值，过期时间，路径和域。路径与域一起构成cookie的作用范围。若不设置过期时间，则表示这

个cookie的生命期为浏览器会话期间，关闭浏览器窗口，cookie就消失。这种生命期为浏览器会话期的cookie被称为会话cookie。

会话cookie一般不存储在硬盘上而是保存在内存里，当然这种行为并不是规范规定的。若设置了过期时间，浏览器就会把cookie

保存到硬盘上，关闭后再次打开浏览器，这些cookie仍然有效直到超过设定的过期时间。存储在硬盘上的cookie可以在不同的浏

览器进程间共享，比如两个IE窗口。而对于保存在内存里的cookie，不同的浏览器有不同的处理方式

### cookie 的存储

- 以键值对（dict）方式存储。如 {"sessionkey": "123"}
- 浏览器会自动对于它进行解析。

## session

session 机制采用的是在服务器端保持状态的方案

### session 机制

服务器端保持状态的方案在客户端也需要保存一个标识，所以 session 机制可能需要借助于 cookie 机制，
来达到保存标识的目的，但实际上它还有其他选择（如 session storage 和 local storage）。

session机制是一种服务器端的机制，服务器使用一种类似于散列表的结构（也可能就是使用散列表）来保存信息。

          当程序需要为某个客户端的请求创建一个session时，服务器首先检查这个客户端的请求里是否已包含了一个session标识

（称为session id），如果已包含则说明以前已经为此客户端创建过session，服务器就按照session id把这个session检索出来

使用（检索不到，会新建一个），如果客户端请求不包含session id，则为此客户端创建一个session并且生成一个与此session相

关联的session id，session id的值应该是一个既不会重复，又不容易被找到规律以仿造的字符串，这个session id将被在本次响应

中返回给客户端保存。保存这个session id的方式可以采用cookie，这样在交互过程中浏览器可以自动的按照规则把这个标识发送给

服务器。一般这个cookie的名字都是类似于SEEESIONID。但cookie可以被人为的禁止，则必须有其他机制以便在cookie被禁止时

仍然能够把session id传递回服务器。

经常被使用的一种技术叫做URL重写，就是把session id直接附加在URL路径的后面。还有一种技术叫做表单隐藏字段。就是服务器

会自动修改表单，添加一个隐藏字段，以便在表单提交时能够把session id传递回服务器。比如：
 
<form name="testform" action="/xxx"> 
<input type="hidden" name="jsessionid" value="ByOK3vjFD75aPnrF7C2HmdnV6QZcEbzWoWiBYEnLerjQ99zWpBng!-145788764"> 
<input type="text"> 
</form> 

实际上这种技术可以简单的用对action应用URL重写来代替。

## cookie 和 session 的区别

cookie 机制采用的是在客户端保持状态的方案，而 session 机制采用的是在服务器端保持状态的方案

- Cookie和Session都是会话技术，Cookie是运行在客户端，Session是运行在服务器端。

- cookie数据存放在客户的浏览器上，session数据放在服务器上。

- Cookie有大小限制以及浏览器在存cookie的个数也有限制，Session是没有大小限制和服务器的内存大小有关。

- Cookie有安全隐患，通过拦截或本地文件找得到你的cookie后可以进行攻击。

- 域的支持范围不一样，比方说a.com的Cookie在a.com下都能用，而www.a.com的Session在api.a.com下都不能用，
    解决这个问题的办法是JSONP或者跨域资源共享。

- Session是保存在服务器端上会存在一段时间才会消失，如果session过多会增加服务器的压力。

所以建议：
   将登陆信息等重要信息存放为 SESSION
   其他信息如果需要保留，可以放在COOKIE中

## 利用 cookie 实现 HTTP 的有状态请求

浏览器 a 向服务器发起请求时，服务器会自动给浏览器 a 回复一个 id，浏览器 a 把 id 放到 cookie
当中，在下一次请求时带上这个 cookie 里的 id 值向服务器发送请求，服务器就知道是哪个浏览器发过来的了。

服务器 a 发回来的 id 会放到服务器 a 的域之下。不能跨域访问 cookie。

如果将用户名和密码直接保存在cookie，可以实现最垃圾最简略版本的自动登录。

## 使用 session 解决 cookie 不安全的问题

> 用户在第一次请求后，浏览器回复的 id 既可以是用户的 user id。
  也可以一段任意的字符串，我们把它叫做 session id。

根据用户名和密码等相关信息，服务器会采用自己的规则生成 session id。这个 session id 保存
在浏览器的 cookie 中。浏览器请求服务器会携带。

- 输入用户名 & 密码
- 调用 login(), 后端程序会根据用户名密码生成 session id。保存在数据库中。
- 用户登录之后，需要通过这个 session id 取出这些基本信息。

通过 session id，用户访问任何一个页面都会携带，服务器就会认识。

### Django 对 session 的处理

Django 的默认表中的 session 表就记录了用户登录时，Django 为用户生成的 session id。

'django.contrib.sessions' 这个 app 会拦截我们每次的 request 请求，在 request 中
找到 session id，然后去数据表中进行查询。

然后通过 session key（session_key 发到浏览器叫做 session id） 去找到session data。
此时直接为我们取出了 user。

在服务器返回浏览器的 response 中也会直接加上 session id。
                          
                       
                       
## cookie、sessionStorage、localStorage 异同点

html5 中 webStorage 包含 sessionStorage 和 localStorage

共同点：
- 都保存在浏览器端，且是同源的

区别：
- cookie 数据始终在同源的http请求中携带，而 webStorage 不会再请求中携带，仅仅在本地存储
- 存储大小区别，cookie 是4k，webStorage 可以达到 5M 甚至更大
- 数据有效时间区别： 
    - sessionStorage 仅仅是会话级别的存储，它只在当前浏览器关闭前有效，不能持久保持；
    - localStorage 始终有效，即使窗口或浏览器关闭也一直有效，除非用户手动删除，其才会失效；
    - cookie 只在设置的 cookie 过期时间之前一直有效。
- 作用域区别：
    - sessionStorage 不在不同的浏览器窗口中共享，即使是同一个页面； 
    - localStorage 和 cookie 在所有同源窗口是共享的
- Web Storage 支持事件通知机制，可以将数据更新的通知发送给监听者。Web Storage 的 api 接口使用更方便。

## web storage和cookie的区别

- Web Storage的概念和cookie相似，区别是它是为了更大容量存储设计的。
    Cookie的大小是受限的，并且每次你请求一个新的页面的时候Cookie都会被发送过去，这样无形中浪费了带宽，
    另外cookie还需要指定作用域，不可以跨域调用。
- 除此之外，Web Storage拥有setItem,getItem,removeItem,clear等方法，不像cookie需要前端开发者
    自己封装setCookie，getCookie。
- 但是Cookie也是不可以或缺的：Cookie的作用是与服务器进行交互，作为HTTP规范的一部分而存在 ，
    而Web Storage仅仅是为了在本地“存储”数据而生。
- Cookies:服务器和客户端都可以访问；大小只有4KB左右；存在有效期，过期后将会删除；
- 本地存储：只有本地浏览器端可访问数据，服务器不能访问本地存储直到故意通过POST或者GET的通道发送到服务器；
    每个域5MB；没有过期数据，它将保留知道用户从浏览器清除或者使用Javascript代码移除
