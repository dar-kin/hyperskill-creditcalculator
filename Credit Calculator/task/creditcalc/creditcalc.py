from math import ceil
from math import floor
from math import log
from math import pow
import argparse
from sys import argv
from string import ascii_lowercase


def find_n(pri, m_pay, inter):
    return ceil(log(m_pay / (m_pay - inter * pri), 1 + inter))


def find_a(pri, n_month, inter):
    return ceil(pri * inter * pow(1 + inter, n_month) / (pow(1 + inter, n_month) - 1))


def find_p(a_pay, n_month, inter):
    return floor(a_pay / (inter * pow(1 + inter, n_month) / (pow(1 + inter, n_month) - 1)))


def calc_d(pri, n_month, inter, curr_month):
    return ceil(pri / n_month + inter * (pri - pri * (curr_month - 1) / n_month))


parser = argparse.ArgumentParser()
parser.add_argument("--type")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")
args = parser.parse_args()
overpay = 0
no_negatives = True
for elem in argv[1:]:
    elem = elem.strip(ascii_lowercase+".-=")
    if elem != "" and float(elem) < 0:
        no_negatives = False
types = ["annuity", "diff"]
if args.type and args.type in types and args.interest and len(argv) == 5 and no_negatives:
    interest = float(args.interest) / 100 / 12
    if args.type == "annuity":
        if not args.principal:
            principal = find_p(float(args.payment),
                               float(args.periods), interest)
            print(f"""Your credit principal = {principal}!
Overpayment = {int(int(args.periods) * float(args.payment) - principal)}""")
        elif not args.periods:
            periods = find_n(float(args.principal),
                             float(args.payment), interest)
            years = int(periods/12)
            month = periods % 12
            if years == 0:
                print(f"You need {month} months to repay this credit!")
            elif month == 0:
                print(f"You need {years} years to repay this credit!")
            else:
                print(f"You need {years} years and {month} months to repay this credit!")
            print(f"Overpayment = {int(periods * float(args.payment) - float(args.principal))}")
        else:
            payment = find_a(float(args.principal),
                             int(args.periods), interest)
            print(f"""Your annuity payment = {payment}!
Overpayment = {int(int(args.periods) * payment - float(args.principal))}""")
    else:
        act_sum = 0
        for i in range(int(args.periods)):
            cur_pay = calc_d(float(args.principal), float(args.periods), interest, i + 1)
            print(f"Month {i+1}: paid out {cur_pay}")
            act_sum += cur_pay
        print(f"Overpayment = {int(act_sum - float(args.principal))}")


else:
    print("Incorrect parameters")
