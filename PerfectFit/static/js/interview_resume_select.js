document.addEventListener("DOMContentLoaded", () => {
  // 데이터 배열
  const data = [
    {
      선택: false,
      제목: "카카오 Node JS 백엔드 개발자 신입 합격을 위한 나의 초특급 필살기 자기소개서",
      직업: "웹 개발자",
      경력: "신입",
      작성날짜: "2024-10-07 20:03",
    },
    {
      선택: false,
      제목: "배달의 민족 Spring 백엔드 개발자 경력 합격을 위한 나의 정성 들인 자기소개서",
      직업: "웹 개발자",
      경력: "경력",
      작성날짜: "2024-10-06 20:03",
    },
    {
      선택: false,
      제목: "세상에서 제일 빠른 타자 속도를 가진 남자의 자기소개서",
      직업: "속기사",
      경력: "신입",
      작성날짜: "2024-10-04 09:03",
    },
    {
      선택: false,
      제목: "백수로 전전긍긍 하다가 나 김승용 일을 한 번 저질러보겠노라 하고 나온 자기소개서",
      직업: "패스트푸드준비원",
      경력: "신입",
      작성날짜: "2023-08-02 20:03",
    },
    {
      선택: false,
      제목: "Figma를 세상에서 제일 잘 다루는 남자. 피세남 한정석입니다.",
      직업: "웹디자이너",
      경력: "신입",
      작성날짜: "2023-05-07 20:03",
    },
    {
      선택: false,
      제목: "아침도 운동, 점심도 운동, 저녁도 운동. 한국산 리쌤 윤성빈입니다.",
      직업: "직업운동선수",
      경력: "경력",
      작성날짜: "2023-02-07 20:03",
    },
  ];

  // 테이블의 tbody를 선택
  const dataBody = document.getElementById("data-body");

  // 데이터를 동적으로 추가
  data.forEach((item) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td><input type="checkbox" /></td>
      <td>${item.제목}</td>
      <td>${item.직업}</td>
      <td>${item.경력}</td>
      <td>${item.작성날짜}</td>
    `;

    dataBody.appendChild(row);
  });
});
