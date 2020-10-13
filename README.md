# PChcker

灵活的参数管理系统

## 架构特性

### 同源

- 保持参数架构内数据的唯一性

```python
class P1(Param):
    name = Field()

    @Field(origin="name")
    def user_name(self, default_value):
        return default_value


p1 = P1()
p1.name = "Acca"
p1.user_name # Acca
```

### 继承

- 提供参数的业务层面的灵活性

```python
class P1(Param):
    name = Field()


class P2(P1):
    @Field(origin="name")
    def user_name(self, default_value):
        return default_value


p2 = P2()
p2.name = "Acca"
p2.user_name # Acca
```

### 集成

- 为大型的参数模型，提供简单性的实现模式

```python
class P1(Param):
    name = Field()


class P2(Param):
    last_update = Field()


class P3(P1, P2):
    @Field()
    def state(self, default_value):
        name = self.name
        last_update = self.last_update.isoformat
        return f"{name}'s docs update at {last_update}"


p1 = P3()
p1.name = "Alice"
p1.last_update = datetime.now()

p1.state # Alice's docs update at 2020-10-13T11:34:06.370998
```

## 数据分层

这里有点参考了redux的设计思维，让所有的状态更新，都保留在`state`层，而`stroe`层只提供基础的入参条件。

### Store层

```python

class FlaskStore(Store, Param):
    @Field()
    def form(self, default_value=None):
        return request.form

    @Field()
    def cookies(self, default_value=None):
        return request.cookies

```

因为field的机制，store层可以轻松的将任何的数据结构进行解构，并组成你想要的形式，这样对于开发人员来说，是十分友好的，因为我们可以定义自己需要的空间，而不是每次都要重新去定义一遍。另外，定义好store层，能够让参数解析的架构层和业务层有较好的分割，毕竟，store管理不算是参数管理的主要功能。

### State层

```python

flask_store = FlaskStore()

class P1(Param):
    user_name = Field(origin="form.uname", store=[flask_store])


p1 = P1()

p1.user_name # will load data from request.form
```

state层默认嵌入在param对象中，可以说，每一个param，就是一个state层的数据实体，因为Field机制，我们可以轻松的变更param层的数据。

## 降级策略

### 参数的降级主要发生在两个主要流程中

1. 参数加载流程
2. 参数解析流程(特性条件下)

为了较好的支撑降级策略，特地采用了`多源点` + `多store`的策略集合，可以实现，按照源点序列或者store序列，不断的降级取值的模式。在选择优先级上，origin > store，因为origin往往体现的是用户使用时候的直接体验，应该是接近用户想法的取值续流。

```python
class TestStore(Store, Param):
    @Field
    def sheet(self, default_value):
        return {
            "a": "123"
        }


class T2Store(Store, Param):
    @Field
    def sheet(self, default_value):
        return {
            "b": "221"
        }


test_store = TestStore()
test_store2 = T2Store()


class P1(Param):
    a = Field(origin=["sheet.b", "c", "sheet.a"], store=[test_store, test_store2])


class P2(Param):
    a = Field(origin="sheet.a", store=[test_store, test_store2])


class P3(Param):
    a = Field(origin=["sheet.a", "sheet.b"], store=[test_store2])


p1 = P1()
p2 = P2()
p3 = P3()

print(p1.a, p2.a, p3.a) # 221 123 221
```
