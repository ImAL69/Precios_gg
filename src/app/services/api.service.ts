import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);

  getHello(): Observable<any> {
    return this.http.get('/api/hello/');
  }

  getJuegos(search?: string): Observable<any[]> {
    const url = search ? `/api/juegos/?q=${search}` : '/api/juegos/';
    return this.http.get<any[]>(url);
  }

  getPrecios(juegoId: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/juegos/${juegoId}/precios/`);
  }

  getCategorias(): Observable<any[]> {
    return this.http.get<any[]>('/api/categorias/');
  }
}
