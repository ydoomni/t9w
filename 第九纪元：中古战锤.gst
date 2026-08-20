<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<gameSystem xmlns="http://www.battlescribe.net/schema/gameSystemSchema" id="9e00-2026-0000-0001" name="第九纪元：中古战锤" revision="1" battleScribeVersion="2.03" authorName="Custom Rules Data Team" type="gameSystem">
  <publications>
    <publication id="a41c-a267-ba00-e748" name="总规则 2026 beta3" shortName="CR-2026β3" publicationDate="2026-06-26" />
    <publication id="d21a-eaaa-a328-4a91" name="奥法宝典 2026 beta2" shortName="AC-2026β2" publicationDate="2026" />
    <publication id="f8f3-d460-2cd6-ff5b" name="传奇人物 2026 beta3" shortName="LC-2026β3" publicationDate="2026" />
  </publications>
  <costTypes>
    <costType id="5d8a-7c3f-2026-0001" name="分" defaultCostLimit="-1" hidden="false" />
  </costTypes>
  <profileTypes>
    <profileType id="56cd-0313-13d5-cdf1" name="全局">
      <characteristicTypes>
        <characteristicType id="562b-23a9-360d-ae04" name="Adv" />
        <characteristicType id="8ddb-90cd-9e85-71fd" name="Mar" />
        <characteristicType id="499e-c6d9-39d7-423f" name="Dis" />
        <characteristicType id="aa55-50fc-2e79-0c6b" name="高度" />
        <characteristicType id="cd43-53b8-82bd-dc5d" name="类型" />
        <characteristicType id="3d37-a07e-a372-6ae7" name="底盘" />
        <characteristicType id="2716-d619-bd6e-c13a" name="模型规则" />
      </characteristicTypes>
    </profileType>
    <profileType id="1c3d-ea19-bd5e-c94e" name="防御">
      <characteristicTypes>
        <characteristicType id="7159-7b93-749c-5e39" name="HP" />
        <characteristicType id="0c48-bbbe-2ce5-366b" name="Def" />
        <characteristicType id="bf53-ee3e-1216-a29e" name="Res" />
        <characteristicType id="21eb-30e6-3a60-8705" name="Arm" />
        <characteristicType id="43dd-edef-870d-73d5" name="装备与规则" />
      </characteristicTypes>
    </profileType>
    <profileType id="eddd-78eb-dea2-b308" name="进攻">
      <characteristicTypes>
        <characteristicType id="6a86-5f60-ea3a-ec3f" name="Att" />
        <characteristicType id="7e3f-edad-c60d-0479" name="Off" />
        <characteristicType id="0260-4f71-8fde-b4f7" name="Str" />
        <characteristicType id="d813-a407-8565-a1ab" name="AP" />
        <characteristicType id="338a-dfb3-3aa8-0aab" name="Agi" />
        <characteristicType id="eb75-8dab-a170-ac80" name="武器与规则" />
      </characteristicTypes>
    </profileType>
    <profileType id="513a-68f7-3306-72c3" name="武器">
      <characteristicTypes>
        <characteristicType id="a6a2-d5db-d969-23d2" name="射程" />
        <characteristicType id="00a7-f52b-407a-5a41" name="射数" />
        <characteristicType id="4609-921f-2288-1eee" name="力量" />
        <characteristicType id="5e4d-cde3-4076-0de2" name="AP" />
        <characteristicType id="f978-e86c-7ac4-5998" name="瞄准" />
        <characteristicType id="aa6e-8dca-45a8-cefe" name="规则" />
      </characteristicTypes>
    </profileType>
    <profileType id="3a56-c4b3-37e5-ca64" name="法术">
      <characteristicTypes>
        <characteristicType id="69b7-a625-3c9d-24f3" name="施法值" />
        <characteristicType id="1fe1-6f22-2270-e9d8" name="射程" />
        <characteristicType id="3a44-3d24-ad22-e21d" name="类型" />
        <characteristicType id="4e62-c95a-9e49-2b98" name="持续时间" />
        <characteristicType id="aba9-1dc6-4945-e9b4" name="效果摘要" />
      </characteristicTypes>
    </profileType>
  </profileTypes>
  <categoryEntries>
    <categoryEntry id="5f81-2ced-95dd-d789" name="人物" hidden="false" />
    <categoryEntry id="1519-32b0-12ac-3a7b" name="核心" hidden="false" />
    <categoryEntry id="61ac-87b4-5333-a8ac" name="特殊" hidden="false" />
    <categoryEntry id="a1b4-905a-754c-c73a" name="劫掠者" hidden="false" />
    <categoryEntry id="5232-b065-1fc2-b616" name="兽栏" hidden="false" />
    <categoryEntry id="5d78-117a-79cb-48ed" name="传奇人物" hidden="false" />
    <categoryEntry id="a1a2-7ec2-3df9-42d2" name="将军" hidden="true">
      <constraints>
        <constraint id="e151-6feb-5cfd-660e" type="min" value="1" field="selections" scope="force" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="false" />
        <constraint id="c2a1-8af2-93b5-00b5" type="max" value="1" field="selections" scope="force" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="false" />
      </constraints>
    </categoryEntry>
    <categoryEntry id="ec1f-c86b-e4fc-fc1a" name="军旗手" hidden="true">
      <constraints>
        <constraint id="d259-e044-bcfb-3e31" type="max" value="1" field="selections" scope="force" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="false" />
      </constraints>
    </categoryEntry>
    <categoryEntry id="6426-3fa4-f04d-590d" name="非人物单位" hidden="true">
      <constraints>
        <constraint id="a724-5355-a510-ee06" type="min" value="4" field="selections" scope="force" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
      </constraints>
    </categoryEntry>
    <categoryEntry id="20b9-642f-0e32-694c" name="法师" hidden="true" />
    <categoryEntry id="11c1-a124-b7fc-5c44" name="祈求女神" hidden="false" />
    <categoryEntry id="2407-657f-4049-7df5" name="暗箭难防" hidden="false" />
    <categoryEntry id="a5d3-0244-6e38-ad11" name="真龙血裔" hidden="false" />
    <categoryEntry id="aebd-b121-50ef-620c" name="天工开物" hidden="false" />
    <categoryEntry id="3743-9974-522c-324a" name="毁灭装置" hidden="false" />
    <categoryEntry id="5cda-4ae9-ca9b-cbf4" name="氏族雷霆" hidden="false" />
    <categoryEntry id="5f73-2713-c55f-c8d2" name="战争引擎" hidden="false" />
    <categoryEntry id="ae69-4b70-141e-b2ac" name="女王之弓" hidden="false" />
    <categoryEntry id="2a89-eb67-de68-9d12" name="古代城械" hidden="false" />
    <categoryEntry id="f70f-8eea-6f00-26b0" name="构装生物" hidden="false" />
    <categoryEntry id="62dc-44fe-599f-546e" name="被埋葬者" hidden="false" />
    <categoryEntry id="3cf8-3e68-f5bf-6852" name="圣赞使者" hidden="false" />
    <categoryEntry id="5579-60a2-1050-07ed" name="天降大石头" hidden="false" />
    <categoryEntry id="0df8-a707-3d27-1d9b" name="又大又狠" hidden="false" />
    <categoryEntry id="1ca3-af1a-0efb-40bb" name="尸山骨海" hidden="false" />
    <categoryEntry id="093f-366a-9f5b-327d" name="狂啸恶灵" hidden="false" />
    <categoryEntry id="5405-afc3-b550-70d3" name="军火库" hidden="false" />
    <categoryEntry id="8bf4-342d-c479-c68c" name="陆行堡垒" hidden="false" />
    <categoryEntry id="c045-8bf4-8a74-e6a9" name="帝国助力" hidden="false" />
    <categoryEntry id="9ed0-5a91-1d81-e91d" name="信仰，钢铁和火药" hidden="false" />
    <categoryEntry id="7206-14bc-69f9-34cd" name="火药桶" hidden="false" />
    <categoryEntry id="131b-9ba7-1e8f-be08" name="驯化野兽" hidden="false" />
    <categoryEntry id="c8f8-7b40-26a3-7d84" name="荒原猛兽" hidden="false" />
    <categoryEntry id="9bf5-d4ce-0acf-1f60" name="禁忌工坊" hidden="false" />
    <categoryEntry id="e15f-c594-8ff5-6085" name="肉体实验室" hidden="false" />
    <categoryEntry id="2ff9-bcce-ee80-f5c7" name="苦难者" hidden="false" />
    <categoryEntry id="6d69-9c60-c109-fadb" name="疾速亡者" hidden="false" />
    <categoryEntry id="30f5-b6d0-d999-0fa8" name="深渊惧兽" hidden="false" />
    <categoryEntry id="9bfd-6949-4e53-d533" name="打捞军火" hidden="false" />
    <categoryEntry id="929f-6a0e-7995-2727" name="游猎战士" hidden="false" />
    <categoryEntry id="ed4c-f75f-8ed2-4335" name="雷霆蜥蜴" hidden="false" />
    <categoryEntry id="c1ea-8178-e1a4-6afc" name="荒野恐怖" hidden="false" />
    <categoryEntry id="4194-0a10-71ff-6d98" name="伏击捕食者" hidden="false" />
    <categoryEntry id="172e-b1d1-a19c-9f5a" name="狂信徒" hidden="false" />
    <categoryEntry id="e408-059c-91b5-4386" name="神灯精灵" hidden="false" />
    <categoryEntry id="12a7-df39-60ed-e641" name="熊神信仰" hidden="false" />
    <categoryEntry id="89aa-3b50-1acd-4ef9" name="霜原恐惧" hidden="false" />
    <categoryEntry id="e0f7-7185-c544-61f8" name="千神使者" hidden="false" />
  </categoryEntries>
  <sharedRules>
    <rule id="37d1-0e5d-dda6-dff3" name="军队分值" hidden="false" publicationId="a41c-a267-ba00-e748">
      <description>军队总分不得超过约定上限；总规则第 9.A 节同时要求不得低于上限超过 10 分。</description>
    </rule>
    <rule id="a24a-68c1-fd5b-3c28" name="军队组成" hidden="false" publicationId="a41c-a267-ba00-e748">
      <description>军表必须包含人物和核心；人物通常至多 40%，核心通常至少 25%，阵营特有分类按种族规则。</description>
    </rule>
    <rule id="f080-c9fb-89e3-8238" name="最小军队规模" hidden="false" publicationId="a41c-a267-ba00-e748">
      <description>除人物外，军队至少包含 4 个单位；战争机器按总规则处理。</description>
    </rule>
    <rule id="2717-f462-1290-dad0" name="战团、野战军与军团" hidden="false" publicationId="a41c-a267-ba00-e748">
      <description>1500-2999 分为战团，3000-7999 分为野战军，8000 分及以上为军团。0-X 上限在战团减半并向上取整，在军团翻倍；全军唯一不变。</description>
    </rule>
    <rule id="8796-8f36-6f43-68ab" name="特殊物品" hidden="false" publicationId="a41c-a267-ba00-e748">
      <description>除非另有说明，特殊物品全军唯一；每个模型最多一个武器附魔、每件护甲最多一个护甲附魔、一般每面旗帜一个附魔、最多两件魔法奇物和一件至尊物品。</description>
    </rule>
  </sharedRules>
  <sharedProfiles>
    <profile id="d951-09b5-a7eb-6116" name="单手武器" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">使用者</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">使用者</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">步行模型与盾牌同用时获得格挡。</characteristic>
      </characteristics>
    </profile>
    <profile id="a50a-d929-f9ae-0389" name="大型武器" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">+2</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">+2</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">双手持用；主动性顺序 0 攻击。</characteristic>
      </characteristics>
    </profile>
    <profile id="4ed6-0924-9a9f-be23" name="戟" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">+1</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">+1</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">双手持用。</characteristic>
      </characteristics>
    </profile>
    <profile id="4e78-9f6f-9b64-71b3" name="骑枪" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">+2</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">+2</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">正面目标时毁灭冲锋（+2 力量、+2 AP、+1 敏捷）；步兵不可用。</characteristic>
      </characteristics>
    </profile>
    <profile id="d9de-6705-b841-f449" name="轻骑枪" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">+1</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">+1</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">正面目标时毁灭冲锋（+1 力量、+1 AP）；步兵不可用。</characteristic>
      </characteristics>
    </profile>
    <profile id="8539-199b-94c2-1c4d" name="成对武器" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">使用者</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">使用者</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">双手持用；+1 攻击次数与+1 进攻技巧；无视格挡。</characteristic>
      </characteristics>
    </profile>
    <profile id="69dc-1585-7044-e087" name="长矛" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">近战</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">使用者</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">+1</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">额外排面攻击；符合条件时首轮再+2 敏捷与+1 AP；仅步兵。</characteristic>
      </characteristics>
    </profile>
    <profile id="2f79-4ffa-f861-f650" name="轻甲" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">-</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">-</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">-</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">+1 护甲。</characteristic>
      </characteristics>
    </profile>
    <profile id="4cc1-7255-87fd-07f0" name="重甲" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">-</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">-</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">-</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">+2 护甲。</characteristic>
      </characteristics>
    </profile>
    <profile id="9820-e4fe-c71d-f337" name="板甲" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">-</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">-</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">-</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">+3 护甲。</characteristic>
      </characteristics>
    </profile>
    <profile id="b343-8100-0440-b178" name="盾牌" hidden="false" typeId="513a-68f7-3306-72c3" typeName="武器" publicationId="a41c-a267-ba00-e748" page="114-116">
      <characteristics>
        <characteristic name="射程" typeId="a6a2-d5db-d969-23d2">-</characteristic>
        <characteristic name="射数" typeId="00a7-f52b-407a-5a41">-</characteristic>
        <characteristic name="力量" typeId="4609-921f-2288-1eee">-</characteristic>
        <characteristic name="AP" typeId="5e4d-cde3-4076-0de2">-</characteristic>
        <characteristic name="瞄准" typeId="f978-e86c-7ac4-5998">-</characteristic>
        <characteristic name="规则" typeId="aa6e-8dca-45a8-cefe">+1 护甲；双手武器对抗近战时不能同时使用。</characteristic>
      </characteristics>
    </profile>
  </sharedProfiles>
  <sharedSelectionEntries>
    <selectionEntry id="a2c8-215d-6cab-406f" name="单手武器" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="b5e5-c2b4-aaec-f120" name="单手武器" hidden="false" targetId="d951-09b5-a7eb-6116" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="08ba-6f4b-32fe-c57c" name="大型武器" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="4c90-9ab5-b199-2677" name="大型武器" hidden="false" targetId="a50a-d929-f9ae-0389" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="1279-77f2-42cd-d247" name="戟" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="8992-5262-1f6b-a3de" name="戟" hidden="false" targetId="4ed6-0924-9a9f-be23" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="75f2-a7d1-89c1-54e2" name="骑枪" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="484b-0f39-28d9-ec7e" name="骑枪" hidden="false" targetId="4e78-9f6f-9b64-71b3" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="f2e4-8107-c24a-39da" name="轻骑枪" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="d023-0986-c7f9-ce08" name="轻骑枪" hidden="false" targetId="d9de-6705-b841-f449" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="f1f0-6ecb-25d6-4096" name="成对武器" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="d8b2-045f-31cf-c4e8" name="成对武器" hidden="false" targetId="8539-199b-94c2-1c4d" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="7e3b-c848-ec85-47e8" name="长矛" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="ae56-ca95-bad4-f067" name="长矛" hidden="false" targetId="69dc-1585-7044-e087" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="6664-4854-40a8-5868" name="轻甲" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="4ef8-6059-8ef9-4dd1" name="轻甲" hidden="false" targetId="2f79-4ffa-f861-f650" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="511d-a856-0174-6e48" name="重甲" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="1148-98bf-0e10-ee80" name="重甲" hidden="false" targetId="4cc1-7255-87fd-07f0" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="c801-61d6-3120-497c" name="板甲" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="aa9d-f123-5f52-a78a" name="板甲" hidden="false" targetId="9820-e4fe-c71d-f337" type="profile" />
      </infoLinks>
    </selectionEntry>
    <selectionEntry id="df66-4c75-f716-89d3" name="盾牌" hidden="false" collective="false" type="upgrade" import="true">
      <infoLinks>
        <infoLink id="7efb-f594-990e-62b2" name="盾牌" hidden="false" targetId="b343-8100-0440-b178" type="profile" />
      </infoLinks>
    </selectionEntry>
  </sharedSelectionEntries>
  <sharedSelectionEntryGroups>
    <selectionEntryGroup id="00e5-8c2d-b6dc-685d" name="魔法派系" hidden="false" collective="false" import="true">
      <selectionEntries>
        <selectionEntry id="d61e-7b4d-35c5-4ed6" name="火焰系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="e882-f688-bede-555b" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="8ca3-97a1-46d7-950d" name="野兽系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="b461-cd32-a753-e8e8" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="e89f-5639-ab6c-ca0d" name="光明系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="66a8-2b53-b9a2-4c62" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="82de-9553-e283-14e8" name="金属系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="e298-71f8-44d1-7a8c" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="0494-ff46-5f60-eea5" name="生命系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="7cb4-49c2-d9b7-e54e" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="8e4f-be17-8be2-5e8e" name="天堂系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="638c-a7dc-a9a2-7ca7" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="5bec-b549-1e7d-e222" name="阴影系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="5778-93c5-710d-1439" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="790c-667c-6459-b724" name="死亡系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="7b18-b9db-b5b4-d7ef" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="51eb-e2de-2985-1f8d" name="高等系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="5b95-8e79-1caa-e01f" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="a9d2-e9d7-19a9-eece" name="黑暗系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="5822-ac7a-40f7-fe5c" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="af8b-9fce-0413-8f2e" name="吸血鬼系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="c22a-a8bc-627b-d0f4" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="4580-95f4-82a7-344b" name="大Waaagh!!!" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="7f80-5cdc-5231-f9b1" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="002e-65ed-7eb2-5de9" name="小Waaaagh!!!" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="3b68-adc4-2345-aaad" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="a6ab-701b-05e7-d1ef" name="斯卡文毁灭法术" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="aba3-5930-14d2-91bf" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c253-5f10-dcf7-20d3" name="斯卡文瘟疫法术" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="f848-e0f4-e1c5-11f0" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6043-a4c1-4cdd-e5af" name="奸奇系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="bbec-d600-a4b3-8602" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6ca9-9900-da37-caef" name="纳垢系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="6b25-93e7-e40e-9405" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="1b30-0ea1-59c0-e0d0" name="色孽系" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="0291-6241-553b-6e26" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c8ef-197d-6bc6-1a1b" name="天劫法术" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" import="true">
          <constraints>
            <constraint id="e12c-7b17-b9aa-5a48" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
          </constraints>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="0" />
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="c125-4582-fbf9-163f" name="通用武器附魔" hidden="false" collective="false" import="true">
      <selectionEntries>
        <selectionEntry id="9885-3a02-ae9c-41a9" name="凯恩神剑" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="ade7-b782-5d98-2089" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="bb04-bb66-dc24-8a27" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="3356-0579-c35b-f7a7" name="凯恩神剑" hidden="false">
              <description>至尊；精灵限定。攻击属性设为 10，并具有强力的特殊伤害与反噬规则。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="200" />
          </costs>
        </selectionEntry>
        <selectionEntry id="9819-4c25-aa87-37cf" name="元素束缚" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="7af1-8db6-aafc-6dcc" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="c267-d8b1-1aa9-f3ea" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="5928-378e-bc6b-d1f7" name="元素束缚" hidden="false">
              <description>对该武器攻击成功的护甲保护与特殊保护必须重投。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="60" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6c5a-0463-648e-1e12" name="屠龙刃" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="6970-7658-8cb0-8dd9" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="ef97-cef9-d2d3-d5ae" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="5e7f-441c-a222-46a3" name="屠龙刃" hidden="false">
              <description>对伟岸获得多重伤害(D3)与闪电反应。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="55" />
          </costs>
        </selectionEntry>
        <selectionEntry id="69c9-e559-a817-f66e" name="勇士之心" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="c028-245f-b556-d3e8" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="1641-7fa7-ddfd-2467" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="6400-8b34-ec65-265b" name="勇士之心" hidden="false">
              <description>+1 攻击次数，力量至少 5，AP 至少 2。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="3136-9667-62f8-351d" name="天杖" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="f754-ebcd-074b-a299" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="7a9c-edf6-edb6-fda3" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="3fe0-5d29-811b-829b" name="天杖" hidden="false">
              <description>骑枪附魔；毁灭冲锋效果改为首轮攻击。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="45" />
          </costs>
        </selectionEntry>
        <selectionEntry id="efa1-7bba-069d-a192" name="行刑者" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="9193-438d-67c7-84ba" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="b26e-30a3-f660-76cf" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="971e-d1bd-3477-e1a4" name="行刑者" hidden="false">
              <description>+6 AP，造伤不优于 3+。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="35" />
          </costs>
        </selectionEntry>
        <selectionEntry id="64d9-1db8-5ba1-d03c" name="杀戮精华" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="1797-25a2-c2b9-52ad" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="5899-045f-5816-7beb" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="1195-aee3-ca27-c42b" name="杀戮精华" hidden="false">
              <description>一次性；一轮近战中+2 Off、+2 Str、+2 AP。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="25" />
          </costs>
        </selectionEntry>
        <selectionEntry id="b098-8687-78d8-65af" name="英雄克星" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="e708-607d-be74-a5a7" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="64ae-9924-c0c7-9097" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="93f5-1bca-ace2-9e8f" name="英雄克星" hidden="false">
              <description>分配给人物或队长的命中+1 力量与+1 AP。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="20" />
          </costs>
        </selectionEntry>
        <selectionEntry id="2b04-a2f2-f1d1-da7a" name="神速敏捷" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="c557-5595-b9d0-145c" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="ab0b-abd4-78da-b7b0" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="659c-301a-4fb5-4d30" name="神速敏捷" hidden="false">
              <description>+2 进攻技巧与+2 敏捷。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="20" />
          </costs>
        </selectionEntry>
        <selectionEntry id="f5c9-a48a-9f5b-86ea" name="锋锐针刺" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="3548-1726-4d00-4a8a" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="84a9-46e2-a7be-eb7a" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="0e1c-1e9e-5761-ac1c" name="锋锐针刺" hidden="false">
              <description>+1 AP。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="10" />
          </costs>
        </selectionEntry>
        <selectionEntry id="071a-1596-21bb-5479" name="天空泰坦弓弦" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="23" import="true">
          <constraints>
            <constraint id="1525-b083-0109-2cf2" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="34fb-eb90-44fd-ed15" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="dac1-d60d-1683-fde5" name="天空泰坦弓弦" hidden="false">
              <description>弓类射击+6 英寸射程、多重命中(D3+1)、装弹。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="760e-7ebf-ff86-7470" name="通用护甲附魔" hidden="false" collective="false" import="true">
      <selectionEntries>
        <selectionEntry id="b543-1951-9e91-4144" name="死亡欺诈" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="ef01-1024-4e89-4394" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="a162-c46a-884a-55c2" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="1856-d793-c1a4-ce97" name="死亡欺诈" hidden="false">
              <description>伟岸不可选；重生(4+)并+1 护甲。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="90" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6e92-9d41-565c-0fa3" name="命运召唤" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="d86b-7a29-5a30-9525" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="7d02-bb02-8eda-9a09" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="d62f-29af-302e-3cbc" name="命运召唤" hidden="false">
              <description>大型构装体或伟岸不可选；魔盾(4+)，护甲设为 3。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="70" />
          </costs>
        </selectionEntry>
        <selectionEntry id="8664-7dff-50b7-ebdd" name="炫目壁障" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="9b86-955e-f344-b392" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="e291-a0a2-19f1-ff1e" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="30c3-c4fe-8449-7c56" name="炫目壁障" hidden="false">
              <description>伟岸不可选；对手重投对穿戴者成功的普通攻击命中。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="60" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6a8f-aa57-0e4e-9da3" name="秘银精华" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="0cc2-9d46-e2ce-5cca" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="b793-0205-a1b4-fa41" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="e428-0934-9c64-8b46" name="秘银精华" hidden="false">
              <description>大型构装体或伟岸不可选；护甲设为 5。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="412e-26ef-0b19-61fe" name="玄武灌注" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="eddf-fc8e-71a3-0772" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="cafa-b894-5de2-cb54" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="5ce0-7a6e-be77-bbdf" name="玄武灌注" hidden="false">
              <description>+1 护甲，魔盾(3+ 对火焰)，重生自动失败。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="b4a7-ee67-727f-0cf2" name="一体防护" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="144d-bdbc-221c-1a5a" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="af0a-ba2d-ab84-955c" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="7793-b417-ddc1-b380" name="一体防护" hidden="false">
              <description>标准模型限定；获得附属与抵抗(近战攻击)。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="11ef-2c7b-9677-520d" name="幽灵守卫" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="f7b9-1158-bc38-0d16" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="fb92-542d-eaf2-8d04" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="5ece-dae2-3264-79b3" name="幽灵守卫" hidden="false">
              <description>重甲或板甲限定；对非魔法攻击+2 护甲。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
        <selectionEntry id="7fb4-c5cb-11fa-147c" name="冶炼合金" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="f20b-43fa-f7de-83c7" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="8c2d-2cdd-8155-87c9" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="fdf0-7c98-c901-1580" name="冶炼合金" hidden="false">
              <description>+1 护甲，-2 进攻技巧。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="15" />
          </costs>
        </selectionEntry>
        <selectionEntry id="e8f0-d641-be45-a618" name="晨昏铸造" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="d037-baa3-6091-1b1f" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="312e-6a03-d596-4f0c" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="8fb9-75b5-201d-31b4" name="晨昏铸造" hidden="false">
              <description>盾牌附魔；可重投护甲保护，但该伤害的特殊保护失败。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="55" />
          </costs>
        </selectionEntry>
        <selectionEntry id="bcb0-f6c8-0b00-f1fd" name="奥法之环" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="3f1e-7578-0d7b-45b3" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="42cd-9f1c-3959-5449" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="4cbf-526f-5a0b-a155" name="奥法之环" hidden="false">
              <description>盾牌附魔；对魔法攻击提升魔盾，至多 3+。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="45" />
          </costs>
        </selectionEntry>
        <selectionEntry id="64b0-9036-23c5-6025" name="藤条守护" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="24" import="true">
          <constraints>
            <constraint id="9fe3-f476-4416-a6ae" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="380a-2441-9ba4-5d21" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="798c-0ec3-7a7c-ce73" name="藤条守护" hidden="false">
              <description>步行限定；不能格挡，额外+1 护甲。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="15" />
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="9a1e-5d37-a8a6-f958" name="通用旗帜附魔" hidden="false" collective="false" import="true">
      <selectionEntries>
        <selectionEntry id="97ca-4ecb-ece4-1710" name="急速战棋" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="568e-7b64-ce54-a4d3" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="2752-f887-0c79-cf63" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="0753-610b-b03e-fe93" name="急速战棋" hidden="false">
              <description>+1 移动、+2 行军。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="854f-b148-bdd1-c2b1" name="剃刀战旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="ae3a-0482-1b98-8043" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="fe77-e0d3-7596-0daa" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="b0bb-81f0-1388-416d" name="剃刀战旗" hidden="false">
              <description>一次性；近战中普通模型普通攻击+1 AP。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="ad6b-94d8-2922-f6ce" name="暴怒战旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="58d8-daef-fcfe-407e" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="ccff-6f76-8ae4-dfd0" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="1697-ae55-6a52-68e4" name="暴怒战旗" hidden="false">
              <description>一次性；步兵行军速度设为 15 英寸并受相应限制。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c3d1-e856-9cdf-14e6" name="失真徽记" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="cff0-4e2d-b169-9988" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="c825-4b6c-e069-abc3" type="max" value="2" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="efc5-0158-5e24-9a06" name="失真徽记" hidden="false">
              <description>一次性；单位获得难以瞄准(2)一回合。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c002-e4c6-f271-d8af" name="游侠战旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="5d9d-6eed-2f1a-448f" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="baa5-9178-d944-3ac5" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="935f-6856-1e9d-c9ed" name="游侠战旗" hidden="false">
              <description>单位获得行者。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="35" />
          </costs>
        </selectionEntry>
        <selectionEntry id="f822-bc9b-21a9-e523" name="保护旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="0b6e-3bec-875d-6d22" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="a901-11dc-078e-2c73" type="max" value="2" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="b134-7f1c-7557-c875" name="保护旗" hidden="false">
              <description>轻甲限定；AP≤2 的攻击不能令护甲差于 6+。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c11d-07f0-71f0-819f" name="永恒烈焰战旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="b657-1f43-c28a-eb02" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="bde7-01f0-ae58-00b4" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="f04b-6d7d-ed3a-1582" name="永恒烈焰战旗" hidden="false">
              <description>一次性；单位获得火焰攻击。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="25" />
          </costs>
        </selectionEntry>
        <selectionEntry id="731c-0bdc-1427-97d5" name="纪律战旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="2707-cf3e-9f1a-fb8e" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="cc55-27c4-4da4-0ea2" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="4719-bfdc-82fc-10ce" name="纪律战旗" hidden="false">
              <description>重投恐慌；有将军或军旗手时自动通过。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="25" />
          </costs>
        </selectionEntry>
        <selectionEntry id="a6b4-2aea-e9f5-67f2" name="猎兽者织锦" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="7ecf-e7b0-ee3e-2126" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="bd5f-6d7b-ab41-47c7" type="max" value="2" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="01b8-608a-6da0-e45a" name="猎兽者织锦" hidden="false">
              <description>单位获得不能被践踏。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="20" />
          </costs>
        </selectionEntry>
        <selectionEntry id="9611-b8a5-56bc-6473" name="巫骨之旗" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="25" import="true">
          <constraints>
            <constraint id="1ddd-c960-9d35-5ca7" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="775b-a571-f868-cefd" type="max" value="3" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="df68-b529-27c2-a3e3" name="巫骨之旗" hidden="false">
              <description>获得或提升魔法抗性。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="10" />
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
    <selectionEntryGroup id="fbe4-da37-42f2-e33e" name="通用魔法奇物" hidden="false" collective="false" import="true">
      <selectionEntries>
        <selectionEntry id="4893-2e82-244f-31ae" name="封印卷轴" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="b68b-eb71-73be-3789" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="c650-14b6-42ff-8de4" type="max" value="2" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="1fc3-2198-fbaa-fa9a" name="封印卷轴" hidden="false">
              <description>一次性；令指定敌方法术在该魔法阶段不能施放。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="65" />
          </costs>
        </selectionEntry>
        <selectionEntry id="b0a6-99ab-d613-9526" name="能量卷轴" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="4c0e-25b5-f05a-12eb" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="3887-5536-abdb-89e8" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="3494-d34d-f66e-a7bb" name="能量卷轴" hidden="false">
              <description>一次性；为一次施法或破法结果加入一颗法术骰。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="b81b-7663-a32a-6f24" name="治疗药剂" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="b36b-8807-65c8-858b" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="58f5-642f-a8c2-5eb1" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="1686-e81e-bdd5-c88b" name="治疗药剂" hidden="false">
              <description>伟岸不可选；一次性恢复 1 HP。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="1f54-0d12-c8ab-8aa9" name="急速药剂" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="5923-1fa6-4559-4d7d" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="39d3-7957-6d16-6ae2" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="e04d-4ac4-5e6e-68fc" name="急速药剂" hidden="false">
              <description>一次性；一回合+3 敏捷。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="20" />
          </costs>
        </selectionEntry>
        <selectionEntry id="6e98-4977-8e33-4851" name="力量药剂" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="2dec-8902-eb39-2b63" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="14a3-8c41-b38d-734d" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="5947-fba5-d6bd-b128" name="力量药剂" hidden="false">
              <description>伟岸不可选；一次性获得粉碎攻击。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="10" />
          </costs>
        </selectionEntry>
        <selectionEntry id="0c93-3756-a47d-149b" name="幸运币" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="2440-da57-a67f-fe71" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="9d3a-52b1-7681-1fdd" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="b29d-ded9-bc7f-45ee" name="幸运币" hidden="false">
              <description>一次性；重投一次失败护甲保护。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="10" />
          </costs>
        </selectionEntry>
        <selectionEntry id="c3ec-a9e8-97aa-8ecb" name="奥木力量之书" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="a446-a0dd-2d33-39c1" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="8301-af4f-fb1d-f889" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="7b5e-a040-de1c-1e0c" name="奥木力量之书" hidden="false">
              <description>至尊；魔法学徒/专家限定，调整已学法术选择。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="1ee9-514c-630d-2c0d" name="赌徒法杖" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="7ebd-6c96-29ad-b764" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="ddc3-aa71-2d8a-31fa" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="c2b9-a308-c8d8-d71b" name="赌徒法杖" hidden="false">
              <description>至尊；法师限定，随机法术选择。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="8b37-0ea8-b59e-a61a" name="禁断法杖" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="3d78-d421-6528-d9d5" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="a7a6-0557-6c42-014e" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="0185-c9b1-3d3b-8e48" name="禁断法杖" hidden="false">
              <description>至尊；法师限定，允许选择两个种族法术。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="62dc-f3f7-974b-6f54" name="防身护符" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="4b96-22a7-108e-1186" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="dfc5-30ff-4671-dd1e" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="df6f-2d44-b83b-dc6b" name="防身护符" hidden="false">
              <description>获得魔盾(5+)。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="30f9-a543-4706-f3d1" name="能量石" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="6adc-14e1-263f-d2a3" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="8cc8-5024-9e97-5115" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="3f2e-7fcc-be1d-4c51" name="能量石" hidden="false">
              <description>获得传导(1)。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="50" />
          </costs>
        </selectionEntry>
        <selectionEntry id="5fb8-1648-67c2-f850" name="水晶球" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="e113-93ed-d25f-b393" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="189f-b4ac-d750-f832" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="b7ca-01cd-2d6f-593b" name="水晶球" hidden="false">
              <description>至尊；敌方魔法阶段首次破法获得+2。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="45" />
          </costs>
        </selectionEntry>
        <selectionEntry id="3d1a-8522-ac28-5ce0" name="巫师帽" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="6172-4567-1b66-c429" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="4d94-dc87-ce5e-1f05" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="19d4-e369-68dc-e867" name="巫师帽" hidden="false">
              <description>非法师限定；随机八风派系并成为魔法学徒。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="f12c-1ed0-ab32-d085" name="龙之法杖" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="9cd1-5ac9-1594-8713" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="762f-f91d-f264-3989" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="c3b3-e0a7-e082-d560" name="龙之法杖" hidden="false">
              <description>获得力量4、AP1、火焰吐息。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="40" />
          </costs>
        </selectionEntry>
        <selectionEntry id="7264-80ae-5827-fc48" name="神秘仆从" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="64af-530c-7a28-cb52" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="1a95-1066-76fd-76cd" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="a8f8-d8df-6c49-f602" name="神秘仆从" hidden="false">
              <description>法师限定；可记录两个派系，不能选择 5、6 号法术。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="35" />
          </costs>
        </selectionEntry>
        <selectionEntry id="9381-7853-29a5-a647" name="战争短杖" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="2669-c44f-2467-3749" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="3848-8668-8409-2622" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="cb53-c551-e835-35c8" name="战争短杖" hidden="false">
              <description>获得法力强度(4/8)的增益充能法术。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="35" />
          </costs>
        </selectionEntry>
        <selectionEntry id="bed0-4737-9728-bf3a" name="独裁皇冠" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="1ccb-6e34-859b-0ad1" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="2693-ef01-8fe5-78cb" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="8f70-8088-c6ad-4946" name="独裁皇冠" hidden="false">
              <description>不当头儿不可选；提升或获得鼓舞人心。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
        <selectionEntry id="9e01-85dc-0a03-2475" name="毁灭的红宝石之戒" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="8868-24bb-d766-6df6" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="6bc8-05b1-aa8b-1722" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="bdae-97b4-ea06-5cdf" name="毁灭的红宝石之戒" hidden="false">
              <description>获得火球术充能法术，法力强度(4/8)。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
        <selectionEntry id="a829-39f2-505c-d829" name="游侠之靴" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="dc26-101d-4f48-e70f" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="bc07-bc9b-ce55-3e06" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="55a0-3565-55a2-08bd" name="游侠之靴" hidden="false">
              <description>步行标准步兵限定；获得行者并提升非飞行移动。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="30" />
          </costs>
        </selectionEntry>
        <selectionEntry id="2540-4cc9-ca87-0390" name="黑曜石护符" hidden="false" collective="false" type="upgrade" publicationId="d21a-eaaa-a328-4a91" page="26-27" import="true">
          <constraints>
            <constraint id="d1ec-5d3c-fb53-3ed5" type="max" value="1" field="selections" scope="parent" shared="true" percentValue="false" includeChildSelections="false" includeChildForces="false" />
            <constraint id="d4ee-40b3-d726-cf04" type="max" value="1" field="selections" scope="roster" shared="true" percentValue="false" includeChildSelections="true" includeChildForces="true" />
          </constraints>
          <rules>
            <rule id="b75d-7f67-db06-5463" name="黑曜石护符" hidden="false">
              <description>获得魔法抗性(2)。</description>
            </rule>
          </rules>
          <costs>
            <cost name="分" typeId="5d8a-7c3f-2026-0001" value="20" />
          </costs>
        </selectionEntry>
      </selectionEntries>
    </selectionEntryGroup>
  </sharedSelectionEntryGroups>
</gameSystem>
