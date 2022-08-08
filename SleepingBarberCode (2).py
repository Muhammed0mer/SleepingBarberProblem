from multiprocessing import Semaphore
import threading    # Import the threading module
import time         # Import the time module
import random       # Import the random module
import concurrent.futures


# Create a global variable to store the number of customers waiting
num_waiting = 0
# Create a global variable to store the number of chairs in the waiting room
num_chairs = 2
barbers=Semaphore(0)
customers=Semaphore(0)
mutex=threading.Lock()

def cutHair():
    print("Barber cutting hair")
    time.sleep(10)
    print("Barber finished cutting hair")

def getHaircut():
    print("customer getting haircut")

def balk():
    print("customer is leaving")

def barber():
    # global customers
    # global barbers
    global num_waiting
    # global mutex

    while True:
        

        print("Barber waiting for customer")
        customers.acquire()
        print("Barber awaken by customer")

        mutex.acquire()
        num_waiting-=1
        barbers.release()
        mutex.release()
        cutHair()
        
        

def customer():
    # global customers
    # global barbers
    global num_waiting

    mutex.acquire()
    if num_waiting < num_chairs:

        num_waiting+=1
        print("Customer arrived")
        customers.release()
        mutex.release()
        
        barbers.acquire()
        getHaircut()
    else:
        mutex.release()
        balk()

def main():
    # global customers
    # global barbers
    global num_waiting
    global num_chairs
    # global mutex

    # Create a thread for the barber
    barber_thread = threading.Thread(target=barber)
    barber_thread.start()

    #Create a thread for each customer
    
    while True:

        time.sleep(5)
        customer_threads = []
        num_chairs = int(input("Enter the number of chairs in waiting room: "))
        n_cust=int(input(("Enter the number of customers that enter the barbershop: ")))
        cust_times=[]
        for i in range(n_cust):
            cust_time=input(f"Enter the time in units at which customer {i+1} arrives: ")
            cust_times.append(int(cust_time))

        for tim in cust_times:
            customer_thread = threading.Thread(target=customer)
            customer_threads.append(customer_thread)
        prev=0
        n=0
        for tim in cust_times:
            time.sleep(tim-prev)
            customer_threads[n].start()
            prev=tim
            n+=1
            
        for customer_thread in customer_threads:
            customer_thread.join()
        
        

    barber_thread.join()

main()

