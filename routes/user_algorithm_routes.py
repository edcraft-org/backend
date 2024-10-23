from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from models.user_defined_algorithm import UserAlgorithm, UserAlgorithmCreate, UserAlgorithmUpdate
from type import List

user_algorithm_router = APIRouter()

@user_algorithm_router.post("/", response_model=UserAlgorithm)
async def add_user_defined_algorithm(algorithm: UserAlgorithmCreate):
    new_algorithm = UserAlgorithm(**algorithm.dict())
    await new_algorithm.insert()
    return new_algorithm

@user_algorithm_router.get("/user/{user_id}", response_model=List[UserAlgorithm])
async def get_algorithms_by_user_id(user_id: str):
    algorithms = await UserAlgorithm.find(UserAlgorithm.user_id == user_id).to_list()
    if not algorithms:
        raise HTTPException(status_code=404, detail="No algorithms found for this user")
    return algorithms

@user_algorithm_router.get("/{algorithm_id}", response_model=UserAlgorithm)
async def get_user_defined_algorithm_by_id(algorithm_id: str):
    algorithm = await UserAlgorithm.get(PydanticObjectId(algorithm_id))
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    return algorithm

@user_algorithm_router.delete("/{algorithm_id}", response_model=str)
async def delete_user_defined_algorithm(algorithm_id: str):
    algorithm = await UserAlgorithm.get(PydanticObjectId(algorithm_id))
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    await algorithm.delete()
    return f"Algorithm {algorithm_id} deleted successfully"

@user_algorithm_router.put("/{algorithm_id}", response_model=UserAlgorithm)
async def update_user_defined_algorithm(algorithm_id: str, update_data: UserAlgorithmUpdate):
    algorithm = await UserAlgorithm.get(PydanticObjectId(algorithm_id))
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    
    update_data_dict = update_data.dict(exclude_unset=True)
    for key, value in update_data_dict.items():
        setattr(algorithm, key, value)
    
    await algorithm.save()
    return algorithm
