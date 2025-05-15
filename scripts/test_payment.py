import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from users.mpesa.payment import Payment

if __name__ == "__main__":
    print(Payment.get_token())
    Payment().stk_push("254111582527", 1)