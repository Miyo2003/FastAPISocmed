import os
from pydantic import TypeAdapter
from ..database.neo4j import driver
from ..models.group import GroupCreate
from ..serializers.group_serializer import GroupSerializer

class GroupService:
    def __init__(self):
        self.driver = driver
    
    async def create_group(self, group_data: GroupCreate) -> dict:
        """Create new group with members"""
        serialized_data = GroupSerializer.deserialize(group_data)
        
        with self.driver.session() as session:
            result = session.run(
                """
                CREATE (g:Group {
                    name: $name,
                    created_at: datetime()
                })
                WITH g
                UNWIND $member_ids AS memberId
                MATCH (u:User {id: memberId})
                CREATE (u)-[:MEMBER_OF]->(g)
                RETURN g
                """,
                name=serialized_data["name"],
                member_ids=serialized_data["member_ids"]
            )
            group_record = result.single()["g"]
            
            return GroupSerializer.serialize(group_record)