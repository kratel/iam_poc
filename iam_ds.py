# Define the data structure to use for IAM permissions
import datetime

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

def move_to_escrow(iam, iam_escrow, member):
	iam_escrow[member] = iam[member]
	iam_escrow[member]['archived_ts'] = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp()).strftime('%Y-%m-%dT%H:%M:%S')
	del iam[member]
	