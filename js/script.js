document.addEventListener('DOMContentLoaded', () => {
    const submitBtn = document.getElementById('submitBtn');
    const diaryInput = document.getElementById('diaryInput');
    const resultSection = document.getElementById('resultSection');
    const correctedText = document.getElementById('correctedText');
    const explanation = document.getElementById('explanation');

    if (submitBtn) {
        submitBtn.addEventListener('click', async () => {
            const text = diaryInput.value.trim();

            if (!text) {
                alert("내용을 입력해주세요!");
                return;
            }

            // 로딩 표시
            resultSection.style.display = 'block';
            correctedText.innerText = "AI가 분석 중입니다...";
            explanation.innerText = "잠시만 기다려주세요.";

            try {
                const response = await fetch('/api/correction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ diary: text })
                });

                const data = await response.json();

                if (data.error) {
                    correctedText.innerText = "오류가 발생했습니다.";
                    explanation.innerText = data.error;
                } else {
                    // 백엔드 파이썬에서 보내주는 키값(corrected, explanation) 출력
                    correctedText.innerText = data.corrected || "교정된 내용이 없습니다.";
                    explanation.innerText = data.explanation || "설명이 없습니다.";
                }
            } catch (error) {
                console.error("Error:", error);
                correctedText.innerText = "서버 연결 오류가 발생했습니다.";
                explanation.innerText = "잠시 후 다시 시도해주세요.";
            }
        });
    }
});