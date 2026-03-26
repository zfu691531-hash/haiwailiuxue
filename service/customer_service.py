"""服务层 - 客户业务逻辑处理"""

from typing import Dict, Any
from dao.database import CustomerDAO


class CustomerService:
    """客户服务类"""
    
    def __init__(self):
        self.dao = CustomerDAO()
    
    def save_customer_judge(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        保存客户研判数据
        
        Args:
            customer_data: 客户研判数据字典
            
        Returns:
            包含处理结果的字典
        """
        try:
            # 设置固定值
            customer_data['source'] = 'client_judge'
            customer_data['creator'] = 'system'
            
            # 将原始数据转为JSON字符串
            raw_data = str(customer_data.get('raw_data', customer_data))
            
            # 调用DAO插入数据
            customer_id = self.dao.insert_customer(
                name=customer_data.get('name', ''),
                creator=customer_data['creator'],
                customer_age=customer_data.get('customer_age', 0),
                customer_gender=customer_data.get('customer_gender', ''),
                customer_fund=customer_data.get('customer_fund', ''),
                customer_address=customer_data.get('customer_address', ''),
                source=customer_data['source'],
                raw_data=raw_data,
                is_target=customer_data.get('is_target', 3),
                judge_reason=customer_data.get('judge_reason', '')
            )
            
            return {
                'code': 200,
                'msg': '客户研判数据保存成功',
                'data': {
                    'customer_id': customer_id
                }
            }
            
        except Exception as e:
            return {
                'code': 500,
                'msg': f'保存失败：{str(e)}',
                'data': None
            }
    
    def __del__(self):
        """析构函数，关闭数据库连接"""
        self.dao.close_connection()
