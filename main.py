import pandas as pd



class orders:
    def __init__(self, data_file):
        self.orders = pd.read_csv(data_file)

    def print_orders(self):
        removed_orders=self.orders[(self.orders.Type == "Remove")].Id.to_list()
        print(self.orders[(~self.orders.Id.isin(removed_orders))])

    def add_order(self,order,price,quantity):
        id = self.orders['Id'].max() + 1 
        new_order = pd.DataFrame({'Id':[id], 'Order':[order], 'Type':['Add'], 'Price':[float(price)],'Quantity':[int(quantity)]})
        self.orders = pd.concat([self.orders,new_order], ignore_index=True)
        if order == "Buy":
            opposite_order = "Sell"
            ascending_order = True
        else:
            opposite_order = "Buy"
            ascending_order = False
        removed_orders=self.orders[(self.orders.Type == "Remove")].Id.to_list()
        best_orders = self.orders[(self.orders.Order==opposite_order)&(~self.orders.Id.isin(removed_orders))]

        best_orders=best_orders.sort_values(by=["Price"], ascending=[ascending_order])
        cum_sum = best_orders["Quantity"].cumsum()
        min_cum_sum = cum_sum[(cum_sum > int(quantity))].min()
      
        best_orders = best_orders[best_orders.Quantity.cumsum()<= min_cum_sum]
        if best_orders.empty:
            print(f"No {opposite_order} orders yet")
        else:
            print(f"Top {opposite_order} orders for you:")

            print(best_orders.to_string())

    def remove_order(self,id):
        order_to_remove = self.orders[(self.orders.Id == int(id)) & (self.orders.Type == "Add")]
        if order_to_remove.empty:
            print(f"There is no order with id {id}")
            return
        
        if self.orders[(self.orders.Id == int(id)) & (self.orders.Type == "Remove")].empty :
            new_order = pd.DataFrame({'Id':[id], 'Order':[order_to_remove.iloc[0].Order], 'Type':['Remove'], 'Price':[order_to_remove.iloc[0].Price],'Quantity':[order_to_remove.iloc[0].Quantity]})
            self.orders = pd.concat([self.orders,new_order])
            print(f"Order {id} removed")
        else:
            print("Order already removed")
            return
    

  

def main():
    #Create data structure to store orders
    orders_data = orders('data.csv')
    print(orders_data.orders.to_string())
    while(True):
        print("\n-----\nMenu:\n1. Add order\n2. Remove order\n3. Show active orders\n4. Exit\n-----")
        option = input("Option: ")
        match option:
            case "1":
                orders_data.add_order(input("Order (Buy/Sell): "),input('Price: '),input("Quantity: "))
                

            case "2":
                orders_data.remove_order(input("Id:"))
            
            case "3":
                orders_data.print_orders()
            
            case "4":
                return


if __name__=="__main__":
    main()