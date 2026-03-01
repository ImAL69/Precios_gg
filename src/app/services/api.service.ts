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

  getJuegos(search?: string, categoriaId?: number | string): Observable<any[]> {
    let url = `/api/juegos/`;
    const params: string[] = [];
    if (search) params.push(`q=${search}`);
    if (categoriaId && categoriaId !== '0') params.push(`categoria=${categoriaId}`);

    if (params.length > 0) url += `?${params.join('&')}`;

    return this.http.get<any[]>(url);
  }

  getPrecios(juegoId: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/juegos/${juegoId}/precios/`);
  }

  getCategorias(): Observable<any[]> {
    return this.http.get<any[]>('/api/categorias/');
  }
}
