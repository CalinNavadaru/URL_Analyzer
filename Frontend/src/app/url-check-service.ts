import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Results {
  count: number;
  next: string | null;
  previous: string | null;
  results: URLCheck[];
}
export interface URLCheck {
  id: number;
  url: string;
  verdict: string;
  checked_at?: string;
  user_feedback?: string;
}

@Injectable({
  providedIn: 'root',
})
export class UrlCheckService {
  private API_URL = 'http://127.0.0.1:8000/api/urlchecks/';

  constructor(private http: HttpClient) {}

  checkUrl(url: string): Observable<URLCheck> {
    return this.http.post<URLCheck>(this.API_URL, { url });
  }

  getAll(page: number = 1, size?: number): Observable<Results> {
    let params = new HttpParams().set('page', page);
    if (size) {
      params = params.set('size', size);
    }
    return this.http.get<Results>(this.API_URL, { params });
  }

  delete(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}${id}/`);
  }

  update(id: number, data: Partial<URLCheck>): Observable<URLCheck> {
    return this.http.patch<URLCheck>(`${this.API_URL}${id}/`, data);
  }

  reanalyze(id: number): Observable<URLCheck> {
    return this.http.post<URLCheck>(`${this.API_URL}${id}/reanalyze/`, {});
  }
}
