import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SteamService {
  private http = inject(HttpClient);

  searchGames(term: string = 'action'): Observable<any> {
    return this.http.get(`/api/steam/search/?q=${term}`);
  }

  getGameDetails(appId: number): Observable<any> {
    return this.http.get(`/api/steam/details/${appId}/`);
  }
}
