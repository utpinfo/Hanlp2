declare
  cursor c_products is
    select *
      from (select distinct t.*, rownum as rn
               from (select product_name
                        from wsm_product_v
                       where organization_id = 7811
                         and language_id = 2
                       group by product_name
                       order by product_name desc) t
              where rownum <= 1000 -- 先限制上限，避免全表掃描
             )
     where rn between 801 and 1000;
  v_product_name varchar2(300);
  v_line         varchar2(30000);
  v_char         varchar2(400);
begin
  dbms_output.enable(null);
  -- 遍历产品表
  for rec in c_products loop
    v_product_name := rec.product_name;
    -- 输出固定前缀 "查询"
    dbms_output.put_line('查 O');
    dbms_output.put_line('询 O');
  
    -- 逐字符处理产品名称
    for i in 1 .. length(v_product_name) loop
      v_char := substr(v_product_name, i, 1);
      if regexp_like(v_char, '[[:alnum:]\u4e00-\u9fa5]') then
        --1. [:alnum:] = 英文 + 數字,  2.\u4e00-\u9fa5 = 常用中文 Unicode 區間
        v_line := substr(v_product_name, i, 1) || ' ' || case
                    when i = 1 then
                     'B-PRODUCT'
                    else
                     'I-PRODUCT'
                  end;
        dbms_output.put_line(v_line);
      end if;
    end loop;
  
    -- 输出固定后缀 "库存"
    dbms_output.put_line('库 O');
    dbms_output.put_line('存 O');
    -- 句子间空行
    dbms_output.put_line(' ');
  end loop;
end;
