async function checkDiary() {
    const diaryText = document.getElementById('diary-input').value;
    const resultArea = document.getElementById('result-area');
    const correctedText = document.getElementById('corrected-text');
    const explanationText = document.getElementById('explanation-text');

    if (!diaryText.trim()) {
        alert("일기를 입력해주세요!");
        return;
    }

    // 로딩 표시
    correctedText.innerText = "AI가 생각 중입니다...";
    explanationText.innerText = "잠시만 기다려주세요.";

    try {
        const response = await fetch('/api/correction', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ diary: diaryText })
        });

        const data = await response.json();

        if (data.error) {
            correctedText.innerText = "오류가 발생했습니다.";
            explanationText.innerText = data.error;
        } else {
            // 화면에 결과 뿌려주기
            correctedText.innerText = data.corrected || "교정된 문장이 없습니다.";
            explanationText.innerText = data.explanation || "설명이 없습니다.";
        }
    } catch (error) {
        correctedText.innerText = "서버 연결 오류가 발생했습니다.";
        explanationText.innerText = error.message;
    }
}