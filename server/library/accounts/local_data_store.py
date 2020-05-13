from library.accounts.account import Account
from library.accounts.data_store import DataStore
from library.multi_key_dict import MultiKeyDict
from library.utils import require_open


class AccountEntry:
  def __init__(self, account_id, account, hashed_password):
    self._account_id = account_id
    self._account = account
    self._hashed_password = hashed_password

  @property
  def account_id(self):
    return self._account_id

  @property
  def email_address(self):
    return self._account.email_address

  @property
  def account(self):
    return self._account

  @property
  def hashed_password(self):
    return self._hashed_password


AccountEntry.NONE = AccountEntry(Account.NONE.id, Account.NONE, '')


class LocalDataStore(DataStore):
  def __init__(self):
    super().__init__()
    self._accounts = MultiKeyDict(['account_id', 'email_address'])

  def startup(self):
    pass

  def shutdown(self):
    pass

  @require_open
  async def load_account_id_by_email(self, email_address):
    account_entry = self._accounts.get('email_address', email_address)
    return account_entry.account_id

  @require_open
  async def store_account(self, account_id, email_address, hashed_password):
    account = Account(account_id, email_address)
    self._accounts.add(AccountEntry(account_id, account, hashed_password))

  @require_open
  async def load_account(self, account_id):
    account_entry = self._accounts.get('account_id', account_id)
    return account_entry.account

  @require_open
  async def load_password(self, account_id):
    account_entry = self._accounts.get('account_id', account_id)
    return account_entry.hashed_password
