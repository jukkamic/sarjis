import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { ComicComponent } from './comic/comic.component';
import { ComicService } from './comic.service';
import { RouterModule, Routes } from '@angular/router';
import { ComicListComponent } from './comic-list/comic-list.component';

const routes: Routes = [
  { path: 'sarjis/:id', component: ComicComponent },
  { path: '', component: ComicListComponent, pathMatch: 'full' },
];

@NgModule({

  declarations: [
    AppComponent,
    ComicComponent,
    ComicListComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
  ],
  providers: [ComicService],
  bootstrap: [AppComponent]
})
export class AppModule { }
