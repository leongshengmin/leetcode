class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        # each account is a connected component (wherein email in the accounts points to the account id)
        # we do something like union-find to union components as long as the 2 components have at least 1 email in common
        # each time we union, we need to modify the accounts list in place to pop the replaced accounts and add the merged account
        # for each account we need to check all other accounts in accounts to see if they belong to the same set
        # we do this n-1 times since we're assuming a fully-connected graph or until there isn't any more merging to be done

        parents = [i for i in range(len(accounts))]

        def find(u: int) -> int:
            if u == parents[u]:
                return u
            parents[u] = find(parents[u])
            return parents[u]

        def union(parent: int, child: int):
            par_par = find(parent)
            par_chi = find(child)
            parents[par_chi] = par_par

        email_to_account_id = {}
        # loop through each email in the account and merge account ids to point to a single 'parent' account id
        # this 'parent' account id is the first account id for this email that's already in the map
        for i in range(len(accounts)):
            account = accounts[i]
            name, emails = account[0], account[1:]
            for email in emails:
                if email not in email_to_account_id:
                    email_to_account_id[email] = i
                    continue

                account_id = email_to_account_id[email]
                # merge current account i into the account_id that's already into the map
                # note the direction of merging
                union(account_id, i)

        account_id_to_emails = {}
        # now we need to merge using the account_id as the merge key instead of the email
        # since there will be multiple email keys that share the same account id
        # so we need to merge the account ids to point to the same parent account id
        # this will give us the set of emails belonging to the same parent account id
        for email, account_id in email_to_account_id.items():
            par_account_id = find(account_id)
            emails = account_id_to_emails.get(par_account_id, [])
            emails.append(email)
            account_id_to_emails[par_account_id] = emails

        # format output
        res = []
        for account_id, emails in account_id_to_emails.items():
            name = accounts[account_id][0]
            account = [name] + sorted(emails)
            res.append(account)

        return res
