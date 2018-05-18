#!/usr/bin/env python
#
# Git push checker for pre-receive(Server-side)
# version: v0.9
# * All commit messages should contain messases like
# * issue-123 or ISSUE-#123 or issue#123 or hotfix or forced
# * if push contains tags(like 'git push origin --tags'), it's ok(It skips tags)
#
import sys
import re
import subprocess

#Format:
# "oldref newref branch"
# "oldref newref branch"
# ...

input_lines = sys.stdin.readlines()

#print "Content"
#print input_lines
#print "X"

# Check all commits, skiping tags
all_ok = True

for each_line in input_lines:
    if each_line:
        #print "Content: " + each_line
        (base, commit, ref) = each_line.strip().split()
        valid_commit_msg = False

        if ref[:9] == "refs/tags": # Skip tags
            all_ok = True
            continue

        new_br_push = re.match(r'[^1-9]+', base) #handles new branches being pushed
        if new_br_push:
            all_ok = True
            continue

        revs = base + "..." + commit
        proc = subprocess.Popen(['git', 'rev-list','--oneline','--first-parent', revs], stdout=subprocess.PIPE)
        lines = proc.stdout.readlines()
        if lines:
            for line in lines:
                item = str(line)
                idx = item.index(' ')
                rev = item.split()[0]
                rest = item.split()[1:]
                #tracing
                # remote: Item: 7946999, The rest: ['test', 'msg', 'fixed', 'issue-1']
                print "Debug in pre-receive ... Item: %s, Check these messages: %s" % (rev, rest)
    
                merged = ""
                for word in rest:
                    merged += word

                # Regular Expression - Ignore case and multiline option
                match_any = re.search(r'issue-[0-9]{1,12}|issue#[0-9]{1,12}|issue-#[0-9]{1,12}|hotfix|force', merged, re.I|re.MULTILINE)
                if match_any is not None:
                    valid_commit_msg = True

        #print "\n", valid_commit_msg, new_branch_push, branch_deleted, "\n"

        if valid_commit_msg:
            all_ok = True
            continue
        else:
            all_ok = False
            break

if all_ok: #or new_branch_push or branch_deleted:
    exit(0)
else:
    print "[From My GitLab master] Commit message *MUST* contain one of these pattern: issue-123 or ISSUE-#123 or issue#123 or hotfix or forced"
    exit(1)
