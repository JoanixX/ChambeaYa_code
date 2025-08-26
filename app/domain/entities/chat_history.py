from datetime import datetime

class ChatHistory:
	def __init__(self, id: int, phone_number: str, message_order: int, message_role: str, message: str,
				 created_at: datetime = None, updated_at: datetime = None):
		self.id = id
		self.phone_number = phone_number
		self.message_order = message_order
		self.message_role = message_role
		self.message = message
		self.created_at = created_at
		self.updated_at = updated_at