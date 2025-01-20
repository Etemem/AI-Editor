import http from '../utils/request'
//get有值
export function getTest(params: any) {
  return http.request({
    url: '/test',
    method: 'get',
    params
  })
}

//get无值
export function get(params: any) {
  return http.request({
    url: '/test',
    method: 'get',
    params
  })
}
