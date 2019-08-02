# Assume Jill leaves position at company ABC Co
from iam_ds import *
import pprint
from copy import deepcopy

pp = pprint.PrettyPrinter(indent=4)
pad_num = 60

iam_base = deepcopy(iam)
print("IAM hierarchy for company ABC.co")
pp.pprint(iam)

input("\n" + ("=" * pad_num))

# Option one Freeze account
print("\n\nJill is leaving company, she has some high level permissions so they decide to freeze her account.")
freeze_member(iam, 'jill@abc.co')

print("IAM hierarchy now looks like this.")
pp.pprint(iam)

get_stats(iam)

input("\n" + ("=" * pad_num))

print("\n\nLet's say Jill comes back and her account is unfrozen")
print("At some point the IAM hierarchy will go back to previous state")

unfreeze_member(iam, 'jill_frozen@abc.co')

pp.pprint(iam)

#Option two remove account
print("\n\nSecond option would be to remove her account instead of freezing.")

iam = deepcopy(iam_base)

remove_member(iam, 'jill@abc.co')

print("IAM hierarchy would then look like this.")
pp.pprint(iam)

get_stats(iam)

input("\n" + ("=" * pad_num))

#Escrow concept
iam = deepcopy(iam_base)
print("\n\nJill is leaving company, she has some high level permissions, bindings might be valuable to troubleshoot services she was responsible for")
print("Instead of freezing archive binidngs")

move_iam2escrow(iam, iam_escrow, 'jill@abc.co')
print("IAM hierarchy now looks like this.")
pp.pprint(iam)
get_stats(iam)

print("IAM escrow stores the bindings, no permissions in this hierarchy are executable or tied to accounts")
pp.pprint(iam_escrow)
get_escrow_stats(iam_escrow)

input("\n" + ("=" * pad_num))

print("\n\nIf Jill rejoins company, she must get re-added, but will have no permissons tied to her")
print("If needed escrow can be used to merge permissions back in")

print("\nLet's say Jack needs to take over a service Jill previously managed.")
print("Escrow can be used to review what access Jill had.")

print("Assume Jack must gain all access Jill had.")
print("Escrow used to see bindings and merge access from archive with current active user")
move_escrow2iam(iam_escrow, iam, 'jill@abc.co', 'jack@abc.co', 'additive')

print("Current IAM hierarchy.")
pp.pprint(iam)
get_stats(iam)