export interface ResponseMeta {
  traceId: string;
  timestamp: string;
  version: string;
}

export interface StandardResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  meta?: ResponseMeta;
}

export interface ErrorResponse {
  success: boolean;
  message: string;
  error_code: string;
  meta?: ResponseMeta;
  trace_id?: string;
}
