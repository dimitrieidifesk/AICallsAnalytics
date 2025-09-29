from enum import StrEnum


class CallSessionStatus(StrEnum):
    RECEIVED = "Received"
    IN_PROCESSING = "In processing"
    RECEIVING_TRANSCRIPTION = "Receiving transcription"
    ERROR_RECEIVING_TRANSCRIPTION = "Error receiving transcription"
    RECEIVING_ANALYTICS = "Receiving analytics"
    ERROR_RECEIVING_ANALYTICS = "Error receiving analytics"
    PROCESSING_COMPLETED = "Processing completed"


class LeadQuality(StrEnum):
    QUALIFIED = "QUALIFIED"
    UNQUALIFIED = "UNQUALIFIED"
    UNDETERMINED = "UNDETERMINED"


class RequestTypeOpenAi(StrEnum):
    TRANSCRIPTION = "TRANSCRIPTION"
    ANALYTIC = "ANALYTIC"
    DECODING = "DECODING"


class QueueAction(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"



class PromtMessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"


class TaskStatus(StrEnum):
    PENDING = "pending"
    STARTED = "started"
    RETRY = "retry"
    SUCCESS = "success"
    FAILURE = "failure"

