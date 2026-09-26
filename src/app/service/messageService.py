from app.utils.messageUtil import MessagesUtil
from app.service.llmService import LLMService
from app.service.redisService import RedisService
from app.service.Expense import Expense


class MessageService:
    def __init__(self):
        self.messageUtil= MessagesUtil();
        self.llmService= LLMService()
        self.redisService= RedisService()
    
    def process_message(self, user_id, message):
        # if self.messageUtil.isBankSms(message):
        #     return self.llmService.runLLM(message)
        # else:
        #     return None
        
        if not self.messageUtil.isBankSms(message):
            return None
        
        cache_key= f"ds:message:{user_id}:{message}"
        cached_result = self.redisService.get(cache_key)
        
        if cached_result is not None:
            print("Redis cache HIT")
            # Redis returns dict → convert back to Expense
            print("the hit cache -----------", cached_result)
            print ("Expense(**cached_result) ===== ", Expense(**cached_result))
            return Expense(**cached_result)
        
        print("Redis cache MISS")
        
        
        result= self.llmService.runLLM(message)
        print("RESULT TYPE:", type(result))
        print("SERIALIZE TYPE:", type(result.serialize()))
        print("SERIALIZE VALUE:", result.serialize())
        
        if result is not None:
            print("result.model_dump ------- ", result.model_dump());
            self.redisService.set(cache_key, result.model_dump(), ttl=300)
        
        return result
        
        
        