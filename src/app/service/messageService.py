from app.utils.messageUtil import MessagesUtil
from app.service.llmService import LLMService
from app.service.redisService import RedisService


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
            return cached_result
        
        print("Redis cache MISS")
        
        result= self.llmService.runLLM(message)
        
        if result is not None:
            self.redisService.set(cache_key, result, ttl=300)
        
        return result
        
        
        