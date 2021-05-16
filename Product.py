class Product:

  def __init__(self,name,price):
    self.name=name
    self.price=price


class Store:
    def __init__(self):
        self.store = {"btcusdt": Product("btcusdt", 19), "ethusdt" : Product("ethusdt", 18)}

    def getProductList(self):
        return self.store.values()

    def getPrize(self, name):
        product = self.store.get(name)
        return product.price