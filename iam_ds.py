# Define the data structure to use for IAM permissions
import datetime
import re

"""

This is the data structure I'll be using for my simulation.

iam = { member_a : {
					resource_a: {
									<set of permissions>
					}
				}
		}
"""

iam = { 'john@abc.co' : {
						'storage_bucket_alpha' : {'READ'}
						},
		'jack@abc.co' : {
						'storage_bucket_alpha' : {'READ', 'WRITE'},
						'storage_bucket_archive' : {'READ'}
						},
		'jill@abc.co' : {
						'storage_bucket_alpha' : {'READ', 'WRITE', 'DELETE'},
						'storage_bucket_archive' : {'READ', 'WRITE'},
						'Network_configs' : {'READ'}
						}
	  }

iam_escrow = {}

def freeze_member(iam, member):
	name, domain = member.split('@')
	name += "_frozen"
	frozen_member = '@'.join([name, domain])
	iam[frozen_member] = iam[member]
	del iam[member]

def unfreeze_member(iam, member):
	name, domain = member.split('@')
	if name[-7:] == "_frozen":
		name = name[:-7]
	unfrozen_member = '@'.join([name, domain])
	iam[unfrozen_member] = iam[member]
	del iam[member]

def remove_member(iam, member):
	if member in iam:
		del iam[member]

def remove_binding(iam, member, resource, binding):
	# Assumes iam and member exist
	if binding in iam[member][resource]:
		iam[member][resource].remove(binding)

def remove_resource(iam, member, resource):
	if resource in iam[member]:
		del iam[member][resource]

def move_iam2escrow(iam, iam_escrow, member):
	# members aren't frozen in escrow
	archived_ts = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%dT%H:%M:%S')
	if member not in iam_escrow:
		iam_escrow[member] = iam[member]
		iam_escrow[member]['archived_ts'] = archived_ts
		del iam[member]
	else:
		member += "/" + archived_ts
		iam_escrow[member] = iam[member]
		iam_escrow[member]['archived_ts'] = archived_ts
		del iam[member]

def move_escrow2iam(iam_escrow, iam, archived_member, active_member, mode='additive'):
	# active member must exist
	assert (mode in {'strict', 'additive'}), "mode must be 'strict' or 'additive'"
	if active_member not in iam:
		raise KeyError("active_member must exist in iam")
	else:
		# merge permissions from archived_member into active_member
		del iam_escrow[archived_member]['archived_ts']
		if (not iam[active_member]) or mode == 'strict':
			iam[active_member] = iam_escrow[archived_member]
		else:
			for e_resource in iam_escrow[archived_member]:
				if e_resource in iam[active_member]:
					iam[active_member][e_resource].update(iam_escrow[archived_member][e_resource])
				else:
					iam[active_member][e_resource] = iam_escrow[archived_member][e_resource]

def add_resource_bindings(iam, member, resource, permissions=set()):
	if resource not in iam[member]:
		iam[member][resource] = permissions
	else:
		if not iam[member][resource]:
			iam[member][resource] = permissions
		else:
			iam[member][resource].update(permissions)

def is_valid_member(member):
	if not re.match(r"[^@]+@[^@]+\.[^@]+", member):
		return False
	else:
		return True

def add_member(iam, member, resource=None, permissions=set()):
	if not is_valid_member(member):
		raise ValueError("Invalid member format, expecting email")
	if member not in iam:
		iam[member] = {}
		if not resource:
			return
		else:
			add_resource_bindings(iam, member, resource, permissions)

def get_stats(iam):
	num_members = len(iam)
	num_active_members = 0
	num_frozen_members = 0
	frozen_resources = set()
	resources = set()
	for m in iam:
		name, domain = m.split('@')
		if name.endswith("_frozen"):
			num_frozen_members += 1
		else:
			num_active_members += 1
		for r in iam[m]:
			resources.add(r)
			if name.endswith("_frozen"):
				frozen_resources.add(r)
	num_resources = len(resources)
	num_frozen_resources = len(frozen_resources)
	if num_active_members > 0:
		print("Number of active members: %d" % num_active_members)
	if num_resources > 0:
		print("\tNumber of resources being bound to active members: %d" % num_resources)
	if num_frozen_members > 0:
		print("Number of frozen members: %d" % num_frozen_members)
	if num_frozen_resources > 0:
		print("\tNumber of resources being bound to frozen members: %d" % num_frozen_resources)

def get_escrow_stats(iam_escrow):
	num_archived_members = len(iam_escrow)
	resources = set()
	for m in iam_escrow:
		for r in iam_escrow[m]:
			if r == 'archived_ts':
				continue
			resources.add(r)
	num_resources = len(resources)
	print("Number of archived member permission sets: %d" % num_archived_members)
	print("\tNumber of resources in archived sets: %d" % num_resources)
