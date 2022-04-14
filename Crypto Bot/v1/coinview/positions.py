class Position:

    def __init__(self, price, amount=0, total=0):
        self.price = price

        if amount == 0 and total == 0:
            print('error')

        if amount == 0:
            self.amount = total/price
            self.total = total
        
        if total == 0:
            self.total = price*amount
            self.amount = amount


    def get_price(self):
        return self.price

    def get_amount(self):
        return self.amount

    def get_total(self):
        return self.total

    def __str__(self):
        print("The price was {}, the amount is {}, which totals {}.".format(self.price, self.amount, self.total))

    

class Positions:
    def __init__(self):
        self._positions = list()

    def new_position(self, position):
        self._positions.append(position)

    def average(self):
        price_w = 0
        amount_total = 0
        for i in range(len(self._positions)):
            price_w = price_w + self._positions[i].get_price() * self._positions[i].get_amount()
            amount_total = amount_total + self._positions[i].get_amount()
        
        return price_w/amount_total

    def __str__(self):
        for i in range(len(self._positions)):
            self._positions[i].__str__()



# pc = Position(100,10)

# pos1 = Position(300,amount = 20)
# pos2 = Position(200,total = 30)

# trades = Positions()
# trades.new_position(pc)
# trades.new_position(pos2)
# trades.new_position(pos1)
# trades.__str__()
# print('The avg is {}'.format(trades.average()))
