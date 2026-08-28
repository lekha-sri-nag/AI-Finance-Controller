from models.audit_record import AuditRecord


class AuditService:

    def __init__(self):
        self.records: list[AuditRecord] = []

    def add_record(self, record: AuditRecord) -> None:
        self.records.append(record)

    def get_records(self) -> list[AuditRecord]:
        return self.records

    def get_records_for_entity(
        self,
        entity_type: str,
        entity_id: str
    ) -> list[AuditRecord]:

        return [
            record
            for record in self.records
            if record.entity_type == entity_type
            and record.entity_id == entity_id
        ]