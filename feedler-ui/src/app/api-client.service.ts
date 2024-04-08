import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { SubmitRequest } from './types';
import { environment } from '../environments/environment';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiClientService {
  constructor(private http: HttpClient) {}

  createFeed(request: SubmitRequest) {
    return this.http
      .post<{
        feed_id: string;
      }>(`${environment.apiUrl}/api/v1/create-feed`, request)
      .pipe(map((response) => response.feed_id));
  }
}
