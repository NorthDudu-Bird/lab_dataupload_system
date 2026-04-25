export const roleMap = {
  admin: '系统管理员',
  reviewer: '审核员',
  reporter: '上报员'
}

export const userStatusMap = {
  enabled: '启用',
  disabled: '禁用'
}

export const labStatusMap = userStatusMap

export const equipmentStatusMap = {
  normal: '正常',
  faulty: '故障',
  maintenance: '维护中',
  scrapped: '已报废'
}

export const reportStatusMap = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已驳回'
}

export const normalStatusMap = {
  normal: '正常',
  abnormal: '异常'
}

export const noticeStatusMap = {
  draft: '草稿',
  published: '已发布'
}

export function labelOf(map, value) {
  return map[value] || value || '-'
}

export function tagTypeOf(value) {
  const map = {
    enabled: 'success',
    disabled: 'info',
    normal: 'success',
    abnormal: 'danger',
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    faulty: 'danger',
    maintenance: 'warning',
    scrapped: 'info',
    published: 'success',
    draft: 'info'
  }
  return map[value] || 'info'
}

