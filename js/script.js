document.getElementById('submitBtn').addEventListener('click', async function() {
    const diaryInput = document.getElementById('diaryInput').value;
    const resultSection = document.getElementById('resultSection');
    const correctedText = document.getElementById('correctedText');
    const explanation = document.getElementById('explanation');
    const submitBtn = document.getElementById('submitBtn');

    if (!diaryInput.trim()) {
        alert('일기 내용을 입력해주세요!');
        return;
    }

    submitBtn.textContent = 'AI가 분석 중...';
    submitBtn.disabled = true;
    resultSection.style.display = 'none'; // 새 요청 시 이전 결과 숨김

    try {
        const response = await fetch('/api/correction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ diary: diaryInput }),
        });

        const result = await response.json();

        if (response.ok) {
            resultSection.style.display = 'block';
            // 파이썬에서 보낸 corrected와 explanation을 화면에 넣습니다.
            correctedText.textContent = result.corrected;
            explanation.textContent = result.explanation;
            resultSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            // 에러 발생 시 상세 내용을 알림창으로 띄웁니다.
            console.error('Error Detail:', result.error);
            alert('오류가 발생했습니다: ' + JSON.stringify(result.error));
        }

    } catch (error) {
        console.error('Error:', error);
        alert('서버와 통신 중 오류가 발생했습니다.');
    } finally {
        submitBtn.textContent = 'AI에게 첨삭 받기';
        submitBtn.disabled = false;
    }
});