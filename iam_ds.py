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

iam = { 'jack@abc.co' : {
						'storage_bucket_alpha' : {'READ', 'WRITE'},
						'storage_bucket_archive' : {'READ'}
						},
		'john@abc.co' : {
						'storage_bucket_alpha' : {'READ', 'WRITE', 'DELETE'},
						'storage_bucket_archive' : {'READ', 'WRITE'}
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

def move_to_escrow(iam, iam_escrow, member):
	iam_escrow[member] = iam[member]
	iam_escrow[member]['archived_ts'] = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%dT%H:%M:%S')
	del iam[member]

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
