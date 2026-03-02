import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface URLCheck {
  id?: number;
  url: string;
  verdict: string;
  checked_at?: string;
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

  getAll(): Observable<URLCheck[]> {
    return this.http.get<URLCheck[]>(this.API_URL);
  }
}
