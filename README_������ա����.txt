《勇者學院：畢業之證》遊玩／擴充說明
================================

【怎麼玩】
1. 用 RPG Maker MZ 開啟本專案（或 D:\小遊戲\Project5）。
2. 新遊戲從 Map001「學院校門外」開始。
3. 觀看序章三句吐槽 → 禮堂入學 → 一年級中庭。
4. 進入六間教室找老師考試（各 10 題，共 60 題）。
5. 答題為四選一：
   - 答對：解析 → 戰鬥（較易 troop）→ 勝利後進下一題
   - 答錯：扣血（至少留 1HP）→ 戰鬥（較難）→ 勝利後重考同題
6. 六科全過後中庭綜合考門開啟 → 擊敗教務主任 → 取得一年級通行證。
7. 圖書館／保健室／小賣部有三條不可重刷短支線。

【怎麼加題／加老師】
1. 編輯 data/quiz/grade1.json（或新增 grade2.json）。
2. 每題欄位：id, grade, subject, teacherId, question, options[4],
   answer(0-3), explain, correctMsg, wrongMsg,
   troopIdCorrect, troopIdWrong, rewardType, rewardId
3. teachers 陣列加入新老師（teacherId / badgeItemId / clearSwitchId）。
4. 地圖上老師事件只需插件指令：BraveAcademyQuiz / startExam / teacherId=新ID
5. 不必改插件核心邏輯。

【開關／變數（摘要）】
開關 21 序章結束｜22 入學完成｜23 考試中｜24-29 六科完成
     30 綜合考開放｜31 一年級完成｜32 Boss擊敗｜33-35 支線
變數 31 年級｜32 科目｜33 老師｜34 題號｜35 玩家答案｜36 正確答案
     37 答錯次數｜38 老師完成題數｜39 年級完成老師數｜40 徽章數

【驗證】
python -X utf8 scripts/validate_brave_academy.py .

【部署到本機 Project5】
見 scripts/deploy_to_project5.ps1
