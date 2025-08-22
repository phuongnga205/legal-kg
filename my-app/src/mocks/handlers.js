import { http, HttpResponse } from 'msw';

// DỮ LIỆU GIẢ -mẫu response để frontend test hiển thị ClauseCard + LawyerCard.
const sampleResponse = {
  QUESTION: "How to oppose a bad-faith trademark application in Vietnam?",
  CLAUSES: [
    {
      LAW: {
        ID_LAW: "LAW_2005_2022",
        NAME_EN: "Law on Intellectual Property (amended 2022)",
        NAME_VN: "Luật SHTT (sửa đổi 2022)",
        NAME_JP: "知的財産法（2022年改正）",
        EFFECTIVE_DATE: "2023-01-01",
        EXPIRY_DATE: "",
        STATUS: "effective",
        LINK: "https://vbpl.vn/..."
      },
      ARTICLE: {
        ARTICLE_ID: "ART_0112",
        NUMBER: 112,
        TITLE_EN: "Opposition to applications",
        TITLE_VN: "Phản đối đơn đăng ký",
        TITLE_JP: "異議申立て"
      },
      CLAUSE: {
        CLAUSE_ID: "CLS_0112_3",
        NUMBER: 3,
        TEXT_EN: "Any third party may file an opposition...",
        TEXT_VN: "Bất kỳ bên thứ ba nào cũng có thể nộp phản đối...",
        TEXT_JP: "第三者は…提出できる..."
      }
    }
  ],
  LAWYERS: [
    {
      LAWYER_ID: "L001",
      NAME_EN: "Nguyen A",
      NAME_VN: "Nguyễn A",
      NAME_JP: "グエン・A",
      FIRM: "ABC IP Law",
      SPECIALTY_EN: "Trademark;Opposition;Enforcement",
      SPECIALTY_VN: "Nhãn hiệu;Phản đối;Thực thi",
      SPECIALTY_JP: "商標;異議申立て;執行",
      EMAIL: "contact@abc-ip.vn",
      PHONE: "+84 28 1234 5678",
      LANGUAGES: "EN;JP;VI"
    }
  ]
};

export const handlers = [
  // mock API cho chatbot luật: mỗi lần frontend gọi /ask-ip, MSW sẽ trả về dữ liệu mẫu.
  http.post('/ask-ip', async ({ request }) => {
    let body = {};
    try { body = await request.json(); } catch {}
    console.log('[MSW] /ask-ip hit with body:', body);
    return HttpResponse.json(sampleResponse, { status: 200 });
  }),

  // (giúp phát hiện bug nếu frontend gọi nhầm API.
  http.post('*', ({ request }) => {
    console.warn('[MSW] POST not matched, url =', request.url);
    return HttpResponse.text('MSW catch-all', { status: 418 }); // giúp bạn nhận diện trong Network
  }),
];
