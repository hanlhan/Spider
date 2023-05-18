# 智慧体检爬虫

- `diag`: 诊断设置
- `item`: 项目设置
- `union`: 组合设置
- `package`: 套餐设置

## diag

诊断设置

[疾病目录](http://81.71.41.57:8800/manager/api/dictdiag/diag_menu_get)
[疾病列表](http://81.71.41.57:8800/manager/api/dictdiag/diag_list_get?diag_class_id=934&start=0&page_size=15&keywords=)
[疾病详情](http://81.71.41.57:8800/manager/api/dictdiag/diag_detail_get?diag_id=8462)

```python
# diag_id id
# diag_name 诊断名称
# diag_code 诊断编码
# diag_gender 性别 0-暂无 1-男 2-女
# diag_type_name 诊断类型
# diag_branch_name 所属分支
# status 状态 0-有效 1-停用

# diag_advise 诊断建议
# diag_ail_explain 诊断解释
# diag_ail_group_explain 团体解释
# diag_group_advise 团体建议
# diag_keywords 诊断关键字
```
![](asstes/diag_list.png)
![](asstes/diag_detail_1.png)
![](asstes/diag_detail_2.png)
![](asstes/diag_detail_3.png)

## item

[项目目录](http://81.71.41.57:8800/manager/api/dictitem/item_menu_get)
[项目列表](http://81.71.41.57:8800/manager/api/dictitem/item_list_get?item_class_id=&item_branch_id=&keywords=&start=0&page_size=15)
[项目详情](http://81.71.41.57:8800/manager/api/dictitem/item_info_get?item_id=2051)

```python
# item_class_name 分类名称
# item_branch_name 所属分支

```
