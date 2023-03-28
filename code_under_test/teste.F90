subroutine tst_1(A1,x)
   !! ## brief
   !!
   !! Author: autor
   !!
   !! E-mail: <mailto:email>
   !!
   !! Date: 14Fevereiro2023 17:32
   !!
   !! #####Version: version
   !!
   !! ---
   !! **Full description**:
   !!
   !! brief
   !!
   !! ** History**:
   !!
   !! --- 
   !! ** Licence **: Under the terms of the GNU General Public version 3
   !!   <img src="https://www.gnu.org/graphics/gplv3-127x51.png width="63">
   !!--------------------------------------------------------------------------------------------
!teste para tamanho de linha -------------------------------------------------------------------------------------------------------
   USE mpi;USE modCobvParGF !!------------------------------------------------------------------------------------------------------

   implicit none ; character(len=*), parameter :: p_procedure_name = 'tst' 
   !Parameters:
   
   !!
   
   !subroutine name

   !Variables (input, output, inout)
   real, intent(in) :: A1(:)
   integer, intent(in) :: x
   integer initiate_declaration=10
   
   !Local variables:
   integer :: i, ift

   !Code:

   open(unit=23, file="teste.txt",status="new",action="write");  write(23,*) "teste"

   do i=1,x
      A1(i)= A1(i) * 2.0
   end do

   IF(x==30) then
      A1(30) = 145.7
   else 
      goto 30
   end if 
30 continue
   if(x>6) then
      ift = 7
      write(unit=23,*) ift
   ELSE
      ift = 8
   end if

   select case (x)
   case(1)
      print *, "1"
   case(2)
      print *, "2"
   case default
      print *, 'nao sei'
   end select

   if(x<1) write(unit=23,*) ift

   close(unit=23)

end subroutine tst_1


subroutine ifx(b_teste)
   !! ## teste
   !!
   !! Author: autor
   !!
   !! E-mail: <mailto:email>
   !!
   !! Date: 15Fevereiro2023 09:04
   !!
   !! #####Version: version
   !!
   !! ---
   !! **Full description**:
   !!
   !! teste
   !!
   !! ** History**:
   !!
   !! --- 
   !! ** Licence **: Under the terms of the GNU General Public version 3
   !!   <img src="https://www.gnu.org/graphics/gplv3-127x51.png width="63">
   !!

   IMPLICIT NONE
   !Parameters:
   character(len=*), parameter :: procedureName = 'xxx' 
   
   !! subroutine name
   
   real,  parameter :: g = 9.8 

   !! constante geométrica pi

   !Variables (input, output, inout)
   real, intent(in) :: b_teste

   !Local variables:
   real :: a_Teste = 23 !teste

   character(len=20) :: nome

   !Code:
   a_Teste = 3.45

   a_teste= b_teste
   nome = "Luiz"

end subroutine ifx

module test
   
end module
