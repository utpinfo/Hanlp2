declare
  src_kind varchar2(30) := upper('product');
  cursor c_products is
    select *
      from (select distinct t.*, rownum as rn
               from (select product_name
                        from wsm_product_v
                       where 1 = 1
                            -- and organization_id = 7811
                         and language_id = 2
                         and case
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[A-Za-z]') and
                                    regexp_like(product_name, '[0-9]') and regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '中英文数字符号混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[A-Za-z]') and
                                    regexp_like(product_name, '[0-9]') then
                                '中文字母数字混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[A-Za-z]') and
                                    regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '中文字母符号混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[0-9]') and
                                    regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '中文数字符号混合'
                               when regexp_like(product_name, '[A-Za-z]') and regexp_like(product_name, '[0-9]') and
                                    regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '字母数字符号混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[A-Za-z]') then
                                '中文字母混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[0-9]') then
                                '中文数字混合'
                               when regexp_like(product_name, '[\u4e00-\u9fff]') and regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '中文符号混合'
                               when regexp_like(product_name, '[A-Za-z]') and regexp_like(product_name, '[0-9]') then
                                '字母数字混合'
                               when regexp_like(product_name, '[A-Za-z]') and regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '字母符号混合'
                               when regexp_like(product_name, '[0-9]') and regexp_like(product_name, '[^A-Za-z0-9\u4e00-\u9fff]') then
                                '数字符号混合'
                               else
                                '单一类别'
                             end = '中英文数字符号混合'
                       group by product_name
                       order by product_name desc) t
              where rownum <= 1000 -- 先限制上限，避免全表掃描
             )
     where rn between 1 and 200;
  v_product_name varchar2(300);
  v_line         varchar2(30000);
  v_char         varchar2(400);
begin
  dbms_output.enable(null);
  -- 遍历产品表
  for rec in c_products loop
    v_product_name := rec.product_name;
    v_product_name := regexp_replace(v_product_name, '[^[:alnum:]\u4e00-\u9fa5]', '');
    -- 输出固定前缀 "查询"
    dbms_output.put_line('查 O');
    dbms_output.put_line('询 O');
    -- 逐字符处理产品名称
    for i in 1 .. length(v_product_name) loop
      v_char := substr(v_product_name, i, 1);
      --1. [:alnum:] = 英文 + 數字,  2.\u4e00-\u9fa5 = 常用中文 Unicode 區間
      v_line := substr(v_product_name, i, 1) || ' ' || case
                  when i = 1 then
                   'B-' || src_kind
                  when i = length(v_product_name) then
                   'E-' || src_kind
                  else
                   'I-' || src_kind
                end;
      dbms_output.put_line(v_line);
    end loop;

    -- 输出不同后缀
    dbms_output.put_line('D E-WAREHOUSE');
    dbms_output.put_line('Y I-WAREHOUSE');
    dbms_output.put_line('0 I-WAREHOUSE');
    dbms_output.put_line('1 E-WAREHOUSE');
    dbms_output.put_line('库 O');
    dbms_output.put_line('存 O');
    -- 句子间空行
    dbms_output.put_line(' ');
  end loop;

end;
