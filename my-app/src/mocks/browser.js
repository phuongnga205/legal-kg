import { setupWorker } from 'msw/browser'; //tạo ra một service worker giả chạy trong browser
import { handlers } from './handlers.js'; // danh sách các route mock đã định nghĩa trong file handlers.js
//Worker này sẽ “chặn” mọi HTTP request trong trình duyệt, rồi kiểm tra xem có khớp với handler nào không 
//→ nếu có thì trả dữ liệu giả, nếu không thì để request đi thật.
export const worker = setupWorker(...handlers);
