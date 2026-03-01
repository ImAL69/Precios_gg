import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SteamService {
  private http = inject(HttpClient);

  searchGames(term: string = '', categoryId: string = '0'): Observable<any> {
    let url = `/api/steam/search/?q=${term}`;
    if (categoryId !== '0') {
      url += `&categoria=${categoryId}`;
    }
    return this.http.get(url);
  }

  searchEpicGames(term: string = ''): Observable<any> {
    return this.http.get(`/api/epic/search/?q=${term}`);
  }

  getGameDetails(appId: number): Observable<any> {
    return this.http.get(`/api/steam/details/${appId}/`);
  }
}
