/**
 * 导航工具函数
 */

/**
 * 格式化路由路径
 * @param {string} path - 路由路径
 * @returns {string} 格式化后的路径
 */
export function formatPath(path) {
  // 确保路径以斜杠开头
  if (!path.startsWith('/')) {
    path = '/' + path;
  }
  return path;
}

/**
 * 构建查询字符串
 * @param {Object} params - 查询参数
 * @returns {string} 查询字符串
 */
export function buildQuery(params) {
  if (!params || Object.keys(params).length === 0) {
    return '';
  }

  const query = Object.entries(params)
    .map(([key, value]) => {
      if (value === null || value === undefined) {
        return null;
      }
      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
    })
    .filter(Boolean)
    .join('&');

  return query ? `?${query}` : '';
}

/**
 * 解析查询字符串
 * @param {string} queryString - 查询字符串
 * @returns {Object} 查询参数对象
 */
export function parseQuery(queryString) {
  if (!queryString || queryString === '?') {
    return {};
  }

  // 移除开头的问号
  if (queryString.startsWith('?')) {
    queryString = queryString.substring(1);
  }

  return queryString.split('&').reduce((params, param) => {
    const [key, value] = param.split('=');
    if (key && value) {
      params[decodeURIComponent(key)] = decodeURIComponent(value);
    }
    return params;
  }, {});
}

/**
 * 检查路由是否匹配
 * @param {string} pattern - 路由模式
 * @param {string} path - 当前路径
 * @returns {boolean} 是否匹配
 */
export function matchRoute(pattern, path) {
  // 简单的路由匹配实现
  const patternSegments = pattern.split('/').filter(Boolean);
  const pathSegments = path.split('/').filter(Boolean);

  if (patternSegments.length !== pathSegments.length) {
    return false;
  }

  return patternSegments.every((segment, index) => {
    // 动态参数，如 :id
    if (segment.startsWith(':')) {
      return true;
    }
    return segment === pathSegments[index];
  });
}

/**
 * 提取路由参数
 * @param {string} pattern - 路由模式
 * @param {string} path - 当前路径
 * @returns {Object} 路由参数
 */
export function extractParams(pattern, path) {
  const params = {};
  const patternSegments = pattern.split('/').filter(Boolean);
  const pathSegments = path.split('/').filter(Boolean);

  patternSegments.forEach((segment, index) => {
    if (segment.startsWith(':')) {
      const paramName = segment.substring(1);
      params[paramName] = pathSegments[index];
    }
  });

  return params;
}

/**
 * 导航工具对象
 */
export const navigationUtils = {
  formatPath,
  buildQuery,
  parseQuery,
  matchRoute,
  extractParams
};

export default navigationUtils;
