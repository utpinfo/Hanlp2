declare
  src_kind varchar2(30) := upper('AGENT');
  cursor c_agents is
    select distinct agent_name
      from cmm_agent
     where regexp_like(agent_name, '[\u4e00-\u9fff]')
       and regexp_like(agent_name, '[A-Za-z]')
    union all
    select distinct agent_name
      from cmm_agent
     where rownum < 200;
  v_agent_name varchar2(300);
  v_line       varchar2(30000);
  v_char       varchar2(400);
begin
  dbms_output.enable(null);
  -- 遍历产品表
  for rec in c_agents loop
    for suffix in 1 .. 1 loop
      v_agent_name := rec.agent_name;
      v_agent_name := regexp_replace(v_agent_name, '[^[:alnum:]\u4e00-\u9fa5]', '');
      -- 输出固定前缀 "查询"
      dbms_output.put_line('查 O');
      dbms_output.put_line('询 O');
      -- 逐字符处理产品名称
      for i in 1 .. length(v_agent_name) loop
        v_char := substr(v_agent_name, i, 1);
        --1. [:alnum:] = 英文 + 數字,  2.\u4e00-\u9fa5 = 常用中文 Unicode 區間
        v_line := substr(v_agent_name, i, 1) || ' ' || case
                    when i = 1 then
                     'B-' || src_kind
                    when i = length(v_agent_name) then
                     'E-' || src_kind
                    else
                     'I-' || src_kind
                  end;
        dbms_output.put_line(v_line);
      end loop;

      -- 输出不同后缀
      if suffix = 1 then
        dbms_output.put_line('借 O');
        dbms_output.put_line('样 O');
      end if;
      -- 句子间空行
      dbms_output.put_line(' ');
    end loop;
  end loop;

end;
